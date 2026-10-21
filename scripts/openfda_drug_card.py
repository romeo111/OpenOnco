"""Static drug-card shell; public FDA reports are fetched only by the reader."""
from __future__ import annotations

import html
import json
from functools import lru_cache
from pathlib import Path

from knowledge_base.clients.openfda_client import OpenFDAEventQuery
from scripts.clinical_asset_versions import asset_name


COPY = {
    "en": {
        "title": "Adverse-event reports · openFDA",
        "notice": "Reports mentioning this medicine's names may include other drugs and reactions. They do not establish causality or reaction frequency and do not change OpenOnco treatment rules.",
        "sample": "Load up to 5 reports, newest FDA receipt date first. Drug names and reactions retain the original FDA wording.",
        "source": "Source: FDA · matching reports",
        "about": "About these data",
        "updated": "FDA dataset updated",
        "total": "Reports matching this search",
        "initial": "Not loaded yet",
        "load": "Load FDA reports",
        "refresh": "Refresh reports",
        "retry": "Try again",
        "loading": "Loading reports from FDA…",
        "loaded": "Showing {shown} of {total} matching reports. This is a sample, not a risk estimate.",
        "empty": "No reports matched this search. This does not establish safety.",
        "error": "FDA reports are unavailable right now. Try again or open the source link.",
        "unknown": "Not supplied by FDA",
        "report": "Report",
        "received": "Received by FDA",
        "drugs": "All drugs listed in this report",
        "reactions": "Reactions listed in this report",
        "record_source": "Open original FDA record",
        "noscript": "Enable JavaScript to load reports here, or use the FDA source link.",
        "unsearchable": "A searchable medicine name is not available for this record.",
    },
    "uk": {
        "title": "Повідомлення про побічні реакції · openFDA",
        "notice": "Повідомлення зі згадками назв цього препарату можуть містити інші ліки й реакції. Вони не доводять причинного зв’язку чи частоти реакцій і не змінюють лікувальних правил OpenOnco.",
        "sample": "Завантажте до 5 повідомлень, починаючи з останніх отриманих FDA. Назви ліків і реакцій наведено в оригінальному формулюванні FDA.",
        "source": "Джерело: FDA · відповідні повідомлення",
        "about": "Про ці дані",
        "updated": "Дані FDA оновлено",
        "total": "Повідомлень за цим пошуком",
        "initial": "Ще не завантажено",
        "load": "Завантажити повідомлення FDA",
        "refresh": "Оновити повідомлення",
        "retry": "Спробувати знову",
        "loading": "Завантаження повідомлень із FDA…",
        "loaded": "Показано {shown} із {total} відповідних повідомлень. Це вибірка, а не оцінка ризику.",
        "empty": "За цим пошуком повідомлень не знайдено. Це не підтверджує безпечність.",
        "error": "Повідомлення FDA зараз недоступні. Спробуйте знову або відкрийте посилання на джерело.",
        "unknown": "FDA не вказала",
        "report": "Повідомлення",
        "received": "Отримано FDA",
        "drugs": "Усі препарати, зазначені в повідомленні",
        "reactions": "Реакції, зазначені в повідомленні",
        "record_source": "Відкрити оригінальний запис FDA",
        "noscript": "Увімкніть JavaScript для завантаження повідомлень або відкрийте посилання на FDA.",
        "unsearchable": "Для цього запису немає придатної для пошуку назви препарату.",
    },
}


@lru_cache(maxsize=1)
def assets() -> dict[str, bytes]:
    result = {}
    for suffix in ("js", "css"):
        name = f"openfda-drug-card.{suffix}"
        payload = Path(__file__).with_name(name).read_text(encoding="utf-8").encode("utf-8")
        result[asset_name(name, payload)] = payload
    return result


def write_assets(output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    for name, payload in assets().items():
        (output / name).write_bytes(payload)


def render_openfda_card(drug: dict, *, locale: str = "en") -> str:
    copy = COPY[locale]
    names = drug.get("names") or {}
    try:
        query = OpenFDAEventQuery(
            active_substance=names.get("english") or "",
            brand_names=tuple(names.get("brand_names") or ()),
            limit=5,
        )
    except ValueError:
        return f'<section class="kb-openfda" lang="{locale}" data-original-source><h2>{copy["title"]}</h2><p>{copy["unsearchable"]}</p><a href="https://open.fda.gov/apis/drug/event/">{copy["about"]}</a></section>'
    url = html.escape(query.request_url, quote=True)
    config = html.escape(json.dumps(copy, ensure_ascii=False), quote=True)
    css = next(name for name in assets() if name.endswith(".css"))
    js = next(name for name in assets() if name.endswith(".js"))
    # Protect source wording from the existing automatic display translations.
    return f'''<!-- openfda-drug-card:start -->
<section id="openfda-reports" class="kb-openfda" lang="{locale}" data-original-source translate="no" data-openfda-card data-query-url="{url}" data-copy="{config}" aria-labelledby="openfda-heading">
  <link rel="stylesheet" href="/{css}">
  <h2 id="openfda-heading">{copy["title"]}</h2>
  <p>{copy["notice"]}</p>
  <p class="kb-muted">{copy["sample"]}</p>
  <p class="openfda-links"><a href="{url}" target="_blank" rel="noopener noreferrer">{copy["source"]}</a> · <a href="https://open.fda.gov/apis/drug/event/" target="_blank" rel="noopener noreferrer">{copy["about"]}</a></p>
  <dl class="openfda-metadata"><div><dt>{copy["updated"]}</dt><dd data-openfda-updated>{copy["initial"]}</dd></div><div><dt>{copy["total"]}</dt><dd data-openfda-total>—</dd></div></dl>
  <button type="button" data-openfda-load disabled>{copy["load"]}</button>
  <p data-openfda-status role="status" aria-live="polite" aria-atomic="true">{copy["initial"]}</p>
  <div data-openfda-results hidden></div>
  <noscript><p>{copy["noscript"]}</p></noscript>
  <script src="/{js}" defer></script>
</section>
<!-- openfda-drug-card:end -->'''
