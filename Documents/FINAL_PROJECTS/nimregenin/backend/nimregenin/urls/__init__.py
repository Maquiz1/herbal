# nimregenin/urls/__init__.py

from .demographic_url import urlpatterns as demographic_urls
from .screening_url import urlpatterns as screening_urls
from .enrollment_url import urlpatterns as enrollment_urls
from .crf import urlpatterns as crf_urls
from .utility import urlpatterns as utility_urls
from .visit_url import urlpatterns as visit_urls

app_name = 'nimregenin'  # ← ONLY HERE

urlpatterns = (
    *demographic_urls,
    *screening_urls,
    *enrollment_urls,
    *crf_urls,
    *utility_urls,
    *visit_urls,
)