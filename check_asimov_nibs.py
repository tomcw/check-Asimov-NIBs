import requests

def SaveNIB(url, req):
	fname = 'unknown.nib'
	if url.find('/'):
		fname = url.rsplit('/', 1)[1]

	f = open('NIBs/'+fname, 'wb')
	f.write(req.content)
	f.close()

#==================

def GetAndCheckNIB(line):
	base_url = 'https://mirrors.apple2.org.za/ftp.apple.asimov.net/'
	url = base_url + line.split('/', 1)[1]
	req = requests.get(url, allow_redirects=True)
	savedFile = False

	# Quick NIB sanity check
	NIB1_TRACK_SIZE = 0x1A00
	numTracksInImage = len(req.content) // NIB1_TRACK_SIZE # int=int//int
	if len(req.content) % NIB1_TRACK_SIZE != 0:
		print("Warning: NIB size isn't a whole number of 0x1A00 tracks (size=" + '{:d}'.format(len(req.content)) + ")")
	if numTracksInImage != 35:
		print("Warning: NIB has {:d} tracks".format(numTracksInImage))
	for track in range(numTracksInImage):
		trkBase = track * NIB1_TRACK_SIZE
		for byte in range(NIB1_TRACK_SIZE):
			if req.content[trkBase+byte] != 0xD5: # find 1st D5 in track
				continue
			prologueHdr = 0
			for i in range(3):
				prologueHdr <<= 8
				prologueHdr |= req.content[trkBase+byte]
				byte += 1
				if byte == NIB1_TRACK_SIZE: byte = 0
			if prologueHdr != 0xD5AA96 and prologueHdr != 0xD5AAB5: # ProDOS/DOS 3.3 or DOS 3.2
				print('Warning: T${:02X}'.format(track) + ": NIB image's first D5 header isn't D5AA96 or D5AAB5 (found: " + '{:X}'.format(prologueHdr) + ")")
				if savedFile == False:
					SaveNIB(url, req)
					saveFile = True
			break

#==================

print('Check Asimov NIBs')

f_in = open('site_index.txt','r')
c=0
for line in f_in.readlines():
	# eg. line = './images/games/action/Arcticfox.nib'
	if line.rfind('.nib') >= 0:
		c=c+1
		line = line.split('\n', 1)[0]	# remove trailing newline
		print('{:04d}'.format(c) + ': ' + line)
		GetAndCheckNIB(line)
		if c == 20: break	# debug: just 20
f_in.close()
print('total = ' + str(c))
