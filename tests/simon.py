import solr, logging, time

log = logging.getLogger(__name__)

SOLR_ENDPOINT = "http://feeds.rasset.ie/sitesearch/newsnowlive"
timeout = 0.5
DEBUG = True

sconn = solr.SolrConnection(SOLR_ENDPOINT, debug=DEBUG, timeout=timeout)


def query_solr(**query):
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


count = 0
hammer_amount = 500

def get_document():

    try:


        while (count < hammer_amount):
            mili = int(round(time.time() * 1000))
            query = {
                'q':'categories:"news"',
                'rows':500,
                'mili':mili,
                 }
            result = query_solr(**query)

        return "Test OK"
    except Exception, e:
        raise




if __name__ == "__main__":
    print get_document()

