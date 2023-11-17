from extractor.alp_extractor import ALPExtractor as alp
from datetime import datetime, timedelta

start = datetime.now() -timedelta(days=200)
end = datetime.now() -timedelta(days=1)
print(alp.prices("AAPL",start,end))