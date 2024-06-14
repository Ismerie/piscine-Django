import sys
import antigravity

#test: python3 geohashing.py 37.421542 -122.085589 2005-05-26-10458.68
def main():
    if len(sys.argv) != 4:
        print("Usage: python3 geohashing.py <latitude> <longitude> <date>")
        return
    try:
        latitude = float(sys.argv[1])
    except:
        print("latitude required type: float")
        return
    try:
        longitude = float(sys.argv[2])
    except:
        print("longitude required type:float")
        return
    try:
        date = sys.argv[3].encode()
    except:
        print("date required type: string")
        return
    antigravity.geohash(latitude, longitude, date)
    

if __name__ == '__main__':
    main()