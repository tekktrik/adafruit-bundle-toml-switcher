while read filename; do
    if [ "$1" == "install" ]; then
        echo "Copying $filename to toml_switcher/"
        ln  ./submodules/adabot/tools/$filename ./toml_switcher/$filename;
    elif [ "$1" == "clean" ]; then
        echo "Deleting $filename in toml_switcher/"
        rm ./toml_switcher/$filename;
    fi
done < tools_reqs.txt
