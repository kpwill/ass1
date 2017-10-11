# Monitoring Prober
# takes two command line args, <URL> and <samples_file> (in that order)
# <URL> is the URL we are monitoring
    # must include http protocol (not https, for ex.) and expect port 80
# <samples_file> path to output file

# creates empty file w name given by <samples_file> and writes a single header line:
    # URL=<url>
# runs infinite loop until interrupted by CTRL-C
# every thirty seconds it will:
    # record the time in unix time
        # denoted as $CUR_TIME
    # issue an HTTP/1.1 GET request to URL
        # if the prober doesn't get any response during the 30 seconds or gets
        # any other communication error, it delcares the host DOWN for this sample
        # if it does have an HTTP response, it parses and records HTTP status code
    # write a single line to <samples_file>, two fields COMMA SEPARATED
        # the unix time
        # the HTTP status code, or "-1" if the host was down
            # https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
        # EX: 1442983635,200
    # sleep the duration of the 30 sec allottment

#for README:
    # handling redirects - just reporting original error code
    # must install sys, time, and http.client

import sys, time, http.client


def main():
    #sys.argv = ["http://www.cs.nyu.edu","C:\\Users\\kpwil\\Desktop\\ass1\\sample_output_3.txt"]
    #sys.argv[0] = python file name
    
    if len(sys.argv) < 2:
        print("Not enough arguments.")
        sys.exit

    #handle URLs that have http:// because it messes with the HTTPconnection later
    URL = sys.argv[1]
    if URL.startswith("http://"):
        URL = URL[7:]
        
    output = open(sys.argv[2],"w")
    output.write("URL="+URL+"\n")
    
    initialtime = int(time.time())
    
    while True:
        output = open(sys.argv[2],"a")
        status = getstatuscode(URL)
        
        CUR_TIME = int(time.time())
        output.write(str(CUR_TIME) + "," + str(status) + "\n")
        output.close()
        #print(str(CUR_TIME) + "," + str(status) + "\n")
        
        time.sleep(30.0 - ((time.time() - initialtime) % 30.0))

    
    #figure out how to make it run exactly every 30 seconds
    #test it
    #good job baby

    #output.write("shit")
    output.close()

#credit this? rewrite a little?
def getstatuscode(host, path="/"):
    """ This function retreives the status code of a website by requesting
        HEAD data from the host. This means that it only requests the headers.
        If the host cannot be reached or something else goes wrong, it returns
        None instead.
    """
    try:
        connection = http.client.HTTPConnection(host)
        connection.request("HEAD", path)
        return connection.getresponse().status
    except BaseException:
        return -1

main()
