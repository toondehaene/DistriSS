for size in [10_000, 100_000, 1_000_000, 10_000_000]:
    filedata = bytes(size)
    tempfp = open("file"+str(size/1000)+"k.raw",mode="wb")
    tempfp.write(filedata)
    tempfp.close()
    
