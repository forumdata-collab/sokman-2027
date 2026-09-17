import ephem
import json

def solar_term_date(year, month, day):
    """Compute date (YYYY-MM-DD) when sun reaches given month/day position."""
    # use date-based approximation then refine
    obs = ephem.Observer()
    obs.lat = '22.3'
    obs.lon = '114.17'
    obs.elevation = 0
    sun = ephem.Sun()
    # target: sun enters the solar term. We search around expected date.
    import datetime
    for d in range(-3, 4):
        dt = datetime.date(year, month, day) + datetime.timedelta(days=d)
        obs.date = dt.strftime('%Y/%m/%d') + ' 00:00'
        sun.compute(obs)
        # Check: sun's ecliptic longitude threshold
        lon = ephem.Ecliptic(sun).lon
        print(year, month, day, d, dt, round(float(lon), 2))
        break
    return None

def sun_lon(date):
    obs = ephem.Observer()
    sun = ephem.Sun()
    obs.date = date.strftime('%Y/%m/%d') + ' 12:00'
    sun.compute(obs)
    return float(ephem.Ecliptic(sun).lon) * 180.0 / 3.141592653589793 % 360

def find_term_date(year, target_lon):
    """Find the date in `year` when sun ecliptic longitude crosses target_lon (0-360)."""
    import datetime
    # solar terms targets: 立春=315, 驚蟄=345, 立夏=45, 芒種=75, 立秋=135, 白露=165, 立冬=225, 大雪=255, 小寒=285
    start = datetime.date(year, 1, 1)
    prev = None
    for i in range(0, 380):
        d = start + datetime.timedelta(days=i)
        lon = sun_lon(d)
        if prev is not None:
            # check wrap
            if prev > 300 and target_lon < 100:  # crossing 0/360 boundary
                if lon >= target_lon or lon < prev - 180:
                    return d
            elif prev < target_lon <= lon:
                return d
        prev = lon
    return None

if __name__ == '__main__':
    targets = {'立春': 315, '驚蟄': 345, '立夏': 45, '芒種': 75, '立秋': 135, '白露': 165, '立冬': 225, '大雪': 255}
    result = {}
    for y in range(1930, 2036):
        entry = {}
        for name, lon in targets.items():
            d = find_term_date(y, lon)
            entry[name] = d.strftime('%Y-%m-%d') if d else None
        result[y] = entry
    print(json.dumps(result, ensure_ascii=False, indent=1))
    # sanity: 2027 立春 should be ~2027-02-04
    print('2027:', json.dumps(result.get(2027), ensure_ascii=False))
