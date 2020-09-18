shopt -s nullglob
while :
do
	echo "Trying to find some work"
	for file in *.dat; do
    		filename=${file%%.*}
    		sqrs -r $filename
   		ann2rr -r $filename -a qrs -p N -i s -c > $filename.rr
    		python3 ./calcrr.py $filename.rr
    		rm -rf $filename.dat
    		rm -rf $filename.qrs
    		rm -rf $filename.hea
	done
	echo "No files to work on! Let me take a nap"
	sleep 30s
done
