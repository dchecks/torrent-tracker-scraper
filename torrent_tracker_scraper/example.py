from torrent_tracker_scraper.scraper import Scraper

if __name__ == "__main__":

    # defaultTrackers = open("../udp_trackers.txt", mode='r').read().splitlines()
    scraper = Scraper(
        # trackers=defaultTrackers,
        infohashes=["32729D0D089180D1095279069148DDC27323188B"],
        timeout=5,
    )
    results = scraper.scrape()
    for result in results:
        print(result)
