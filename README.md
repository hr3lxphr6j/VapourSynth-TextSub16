# VapourSynth-TextSub16

Add ass sub with high bit YUV clip.

Requirements:
* fmtconv
* VapourSynth-VSFilter

Usage:

TextSub16(clip, file, [mod=False, charset=None, fps=None, vfr=None, swapuv=None])
* clip: The input clip can be 8-16 bit YUV, and output with 16bit YUV.
* file: ASS file
* mod:   True: Use core.VSFmod.VobSubMod
         False: Use core.xyvsf.TextSub
  default is false
