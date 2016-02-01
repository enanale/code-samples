"""
Query for a list of image URLs from archive.org

Metadata requests are throttled to two at a time to be nice to the Archive :)

"""

import requests
from gevent.pool import Pool
from gevent import monkey

monkey.patch_all()

IMAGE_QUERY_URL = "https://archive.org/advancedsearch.php"

def make_download_url( id, metadata, filename ):
	url = ""
	try:
		url = "https://"+metadata['d1']+metadata['dir']+ "/" +filename
	except:
		url = "https://archive.org/download/"+id+"/"+filename
		print "alt url:", url
	return url

def image_search( text ):
	""" Query archive.org for matching image documents

	Args:
		query (str): The string to search for

	Returns:
		List[str]: List of document ids
	"""
	params = {
		"q": "("+text+") AND mediatype:(image)",
		"rows": 50,
		"page": 1,
		"output": "json",
		'fl[]': "identifier"
	}
	r = requests.get( IMAGE_QUERY_URL, params )
	results = r.json()

	return [doc["identifier"] for doc in results["response"]["docs"]]

def get_image_urls( id ):
	"""	Get image URLs from a document

	Args:
		id (str): Document id

	Returns:
		List(str): List of URLS to the document's images
	"""
	urls = []
	r = requests.get("https://archive.org/metadata/"+id)
	metadata = r.json()
	for f in metadata['files']:
		if f['format'].lower() in ["jpeg","gif"]:
			urls.append( make_download_url(id, metadata, f['name']) )
	return urls

def test():
	ids = image_search("moon")

	# let's be nice to archive.org and limit concurrent requests to 2
	gpool = Pool(2)
	for urls in gpool.imap(get_image_urls, ids):
		print urls

if __name__ == '__main__':
	test()

