import argparse, pathlib

def ctrl2str(ctrl):
  stall = ctrl & 0xf
  yld = ctrl >> 4 & 1
  writeBarrier = ctrl >> 5 & 0x7
  readBarrier = ctrl >> 8 & 0x7
  waitMask = ctrl >> 11 & 0x3f
  waitMaskStr = "--" if waitMask == 0 else f"{waitMask:02x}"
  readStr = "-" if readBarrier == 7 else str(readBarrier + 1)
  writeStr = "-" if writeBarrier == 7 else str(writeBarrier + 1)
  yldStr = "-" if yld == 1 else "Y"
  return f"{waitMaskStr}:{readStr}:{writeStr}:{yldStr}:{stall:x}"


def addControls(inFile, outFile):
  with open(inFile, "r") as fin:
    with open(outFile, "w") as fout:
      start = 0
      for line in fin:
        line = line.rstrip()
        if line.startswith("        /*") and line.endswith(" */"):
          start = line.find("*/  ") + 4
          prevLine = line
        elif start != 0:
          t = int(line[len(line) - 21:-3], 16)
          ctrl = ctrl2str(t >> 41)
          prevLine = prevLine[:start] + ctrl + prevLine[start+10:]
          fout.write(prevLine + '\n')
          fout.write(line + '\n')
          start = 0
        else:
          fout.write(line + '\n')


def addControlsDir(inDir, outDir):
  for inFile in inDir.glob('**/*.sass'):
    if outDir in inFile.parents:
      continue
    outFile = (outDir / inFile.relative_to(inDir)).with_suffix(".ctrl.sass")
    outFile.parents[0].mkdir(parents=True, exist_ok=True)
    addControls(inFile, outFile)


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Add control codes to a SASS disassembly')
  parser.add_argument("-o", type=pathlib.Path, help="Output .sass file or directory")
  parser.add_argument("input", type=pathlib.Path, help="Input .sass file or directory. Must be disassembled with -hex option")
  args = parser.parse_args()
  if args.o == None:
    if args.input.suffix != "":
      args.o = args.input.with_suffix(".ctrl.sass")
    else:
      parser.error('Output directory required if input is a folder')
  elif args.input.suffix == "" and args.o.suffix != "":
    parser.error("Output must be directory if input is a folder")
  
  if args.input.suffix != "" and args.o.suffix == "":
    args.o /= args.input.stem + ".ctrl.sass"
  
  outDir = args.o if args.o.suffix == "" else args.o.parents[0]
  outDir.mkdir(parents=True, exist_ok=True)
  
  if args.input.suffix == "":
    addControlsDir(args.input, outDir)
  else:
    addControls(args.input, args.o)
