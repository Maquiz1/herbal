# nimregenin/urls/crf/__init__.py

from .crf1_url import urlpatterns as crf1_urls
from .crf2 import urlpatterns as crf2_urls
from .crf3 import urlpatterns as crf3_urls
from .crf4 import urlpatterns as crf4_urls
from .crf5 import urlpatterns as crf5_urls
from .crf6 import urlpatterns as crf6_urls
from .crf7 import urlpatterns as crf7_urls

urlpatterns = [
    *crf1_urls,
    *crf2_urls,
    *crf3_urls,
    *crf4_urls,
    *crf5_urls,
    *crf6_urls,
    *crf7_urls
]