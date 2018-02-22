FILES=esp/*

for f in $FILES
do
    echo "Uploading $f file..."
    sudo ../env/bin/ampy -p /dev/ttyUSB0 put $f
done
