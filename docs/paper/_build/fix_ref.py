import re

import glob, os
import sys


def fix_ref_in_file(path: str):

    print(f"fixing: {path}")

    with open(path, mode="r") as file:
        s = file.read()

    regexp = re.compile(
        r"{\\hyperref\[\\detokenize{([^:]+):([^}]+)}\]{\\sphinxcrossref{\(\)}}}"
    )

    s3 = str(s)
    for result in regexp.finditer(s):

        replace = result.group(2).replace("-", ":index:")
        s2 = (
            r"{\hyperref[\detokenize{"
            + result.group(1)
            + r":"
            + result.group(2)
            + r"}]{\ref{"
            + replace
            + r"}}}"
        )
        print(s2)

        s3 = s3.replace(result.group(0), s2)

    with open(path, mode="w") as file:
        file.write(s3)


if __name__ == "__main__":

    dir_path = sys.argv[1]

    print(f"path: {dir_path}")

    for file in glob.glob(os.path.join(dir_path, "*.tex")):
        fix_ref_in_file(path=file)
