for f in ./submodules/adabot/tools/*.py ; do
    filename="$(basename $f)"
    echo "$filename"
    ln  ./submodules/adabot/tools/$filename ./toml_switcher/$filename;
done