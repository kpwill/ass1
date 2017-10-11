#author: Kelly Williams, kpw243


#for README:
    # handling redirects - just reporting original error code
    # must install sys, time, and http.client

import sys, time, http.client

#main function handles file initialization and general implementation of the prober
#makes monitoring requests every 30 seconds and records time + status
def main():
    #sys.argv = ["http://www.cs.nyu.edu","sample_output_3.txt"]
    
    if len(sys.argv) < 2:
        print("Not enough arguments.")
        sys.exit()

    #handle URLs that have http:// because it messes with the HTTPconnection later
    URL = sys.argv[1]
    if URL.startswith("http://"):
        URL = URL[7:]

    #create output file
    output = open(sys.argv[2],"w")
    output.write("URL="+URL+"\n")
    
    initialtime = int(time.time())

    #infinite loop - ended by keyboard interrupt 
    while True:
        output = open(sys.argv[2],"a")

        #get the status code
        status = getstatuscode(URL)
        CUR_TIME = int(time.time())

        #write info to file
        output.write(str(CUR_TIME) + "," + str(status) + "\n")
        output.close()
        
        #print(str(CUR_TIME) + "," + str(status) + "\n")

        #wait REMAINDER of 30 seconds since last request, not a necessarily a full 30s
        time.sleep(30.0 - ((time.time() - initialtime) % 30.0))

    output.close()

#function to retrieve status code of websites
#uses head data to get status code
#returns -1 if any error occurs
def getstatuscode(host, path="/"):
    try:
        connection = http.client.HTTPConnection(host)
        connection.request("HEAD", path)
        return connection.getresponse().status
    except BaseException:
        return -1

#invoke prober
main()
