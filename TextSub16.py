import vapoursynth as vs


def TextSub16(clip, file, mod=False, charset=None, fps=None, vfr=None, swapuv=None):
    core = vs.get_core()
    funcName = 'TextSub16'
    if clip.format.color_family != vs.YUV:
        raise TypeError(funcName + ': only planar YUV input is supported.')
    sw = clip.width
    sh = clip.height
    if clip.format.bits_per_sample != 16:
        src16 = core.fmtc.bitdepth(clip=clip, bits=16)
    else:
        src16 = clip
    src8 = core.fmtc.bitdepth(clip=clip, bits=8)
    yuv444 = src16.format.id == vs.YUV444P16
    yuv422 = src16.format.id == vs.YUV422P16
    yuv420 = src16.format.id == vs.YUV420P16
    if mod:
        src8sub = core.VSFmod.VobSubMod(clip=src8, file=file, swapuv=swapuv)
    else:
        src8sub = core.xyvsf.TextSub(clip=src8, file=file, charset=charset, fps=fps, vfr=vfr, swapuv=swapuv)
    src16sub = core.fmtc.bitdepth(clip=src8sub, bits=16)
    submask = core.std.Expr([src8, src8sub], expr=["x y = 0 255 ?"])
    submaskY = core.std.ShufflePlanes(clips=submask, planes=0, colorfamily=vs.GRAY)
    submaskY = core.fmtc.bitdepth(clip=submaskY, bits=16)
    submaskU = core.std.ShufflePlanes(clips=submask, planes=1, colorfamily=vs.GRAY).fmtc.resample(w=sw, h=sh, sx=0.25,
                                                                                                  kernel="bilinear")
    submaskV = core.std.ShufflePlanes(clips=submask, planes=2, colorfamily=vs.GRAY).fmtc.resample(w=sw, h=sh, sx=0.25,
                                                                                                  kernel="bilinear")
    submask = core.std.Expr([submaskY, submaskU, submaskV], expr=["x y max z max"])
    if yuv444:
        submaskC = submask
    if yuv422:
        submaskC = core.fmtc.resample(submask, w=sw // 2, h=sh, sx=-0.5, kernel="bilinear")
    if yuv420:
        submaskC = core.fmtc.resample(submask, w=sw // 2, h=sh // 2, sx=-0.5, kernel="bilinear")
    submask = core.std.ShufflePlanes(clips=[submask, submaskC, submaskC], planes=[0, 0, 0], colorfamily=vs.YUV)
    res = core.std.MaskedMerge(clipa=src16, clipb=src16sub, mask=submask, planes=[0, 1, 2])
    return res
