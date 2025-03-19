# add_control_codes
Script which adds human readable [control codes](https://github.com/NervanaSystems/maxas/wiki/Control-Codes) to a SASS disassembly.

Input .sass file must be disassembled with `-hex` option. Works on all architectures, starting from Volta (sm_70).

Usage example:
```
nvdisasm -hex kernel.cubin > kernel.sass
python add_control_codes.py kernel.sass -o kernel.ctrl.sass
```
