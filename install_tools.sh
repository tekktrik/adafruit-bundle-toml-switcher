if [ "$1" == "install" ]; then
    for f in ./submodules/adabot/tools/*.py; do
        filename="$(basename $f)"
        echo "Copying $filename to toml_switcher/"
        ln  ./submodules/adabot/tools/$filename ./toml_switcher/$filename;
    done
elif [ "$1" == "clean" ]; then
    for f in ./toml_switcher/*.py; do
        filename="$(basename $f)"
        echo "Deleting $filename in toml_switcher/"
        rm ./toml_switcher/$filename;
    done
fi
