import solr, logging, time, random

log = logging.getLogger(__name__)

SOLR_ENDPOINT = "http://feeds.rasset.ie/sitesearch/newsnowlive"
TIMEOUT = 0.2
DEBUG = True

SOLR_CONN = solr.SolrConnection(SOLR_ENDPOINT,
                                debug=DEBUG,
                                timeout=TIMEOUT,
                                max_retries=3,
                                timeout_increment=0.2
                                )


def query_solr(**query):

    sconn = SOLR_CONN
    if query.has_key('timeout'):
        sconn = solr.SolrConnection(SOLR_ENDPOINT,
                                    debug=True,
                                    timeout=query['timeout'])

    sresponse = None
    try:
        sresponse = sconn.query(**query).__dict__
    except Exception, e:
        raise
    finally:

        if sresponse is None:
            log.warning('SRESPONSE is None', extra={'stack': True, 'solr_query': query})
        else:
            log.info(""" RESPONSE OK   """)

        return sresponse


def get_results(**query):

    # try get the results
    result = query_solr(**query)

    count = 1
    no_of_retries = 3
    timout = TIMEOUT
    timeout_increment = 0.3 #0.2, 0.5, 0.8,

    while (count <= no_of_retries):
        if result:
            break
        else:
            # Increment timeout
            print "Timeout attempt %s " % count
            timout = timout + timeout_increment
            query['timout'] = timout
            result = query_solr(**query)
            print result

        count = count + 1


    return result



def get_index():

    success = 0
    fail = 0
    count = 0
    hammer_amount = 500

    while (count < hammer_amount):

        mili = int(round(time.time() * 1000))
        query = {
            'q':'categories:"news"',
            'rows':500,
            'mili':mili,
             }
        result = get_results(**query)

        if result is None:
            fail = fail + 1
        else:
            success = success + 1

        count = count + 1

    print "%s passed" % success
    print "%s failed" % fail
    return "Test Complete"



def get_index_with_retries():
    success = 0
    fail = 0
    count = 0
    hammer_amount = 500

    while (count < hammer_amount):

        mili = int(round(time.time() * 1000))
        query = {
            'q':'categories:"news"',
            'rows':500,
            'mili':mili,
             }
        result = query_solr(**query)

        if result is None:
            fail = fail + 1
        else:
            success = success + 1

        count = count + 1

    print "%s passed" % success
    print "%s failed" % fail
    return "Test Complete"



def get_document():


    document_ids = [779359, 692109, 606673, 379657, 316094, 299423, 129511, 115963, 101661, 87527, 87540, 74842, 61564, 47400, 36910, 24590, 13957, 6371, 6369]


    success = 0
    fail = 0
    count = 0
    hammer_amount = 500

    while (count < hammer_amount):

        doc_id = random.choice(document_ids)
        mili = int(round(time.time() * 1000))
        query = {
            'q':'id:"%s"'%doc_id,
            'rows':1,
            'isArticle':True,
            'mili':mili,
             }

        result = get_results(**query)

        if result is None:
            fail = fail + 1
        else:
            success = success + 1

        count = count + 1

    print "%s passed" % success
    print "%s failed" % fail
    return "Test Complete"



if __name__ == "__main__":

    # get_document()
    # get_index()
    get_index_with_retries()


