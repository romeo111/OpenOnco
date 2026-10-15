"""Display headings only: preserve each source-defined contact time and action."""

SOURCES = (
    ('Make a note and discuss it at your next visit', 'Занотуйте і обговоріть на наступному візиті'),
    ('Tell your doctor or nurse', 'Повідомте лікаря або медсестру'),
    ('Call the clinic the same day', 'Подзвоніть у клініку того ж дня'),
    ('Contact your doctor or nurse immediately', 'Негайно зв’яжіться з лікарем або медсестрою'),
    ('Go to hospital immediately', 'Звертайтесь у лікарню негайно'),
)

HEADINGS = {
    'es': ('Anótelo y coméntelo en la próxima visita', 'Informe a su médico o al personal de enfermería', 'Llame a la clínica el mismo día', 'Contacte inmediatamente con su médico o con el personal de enfermería', 'Acuda al hospital inmediatamente'),
    'pt': ('Anote e fale sobre isso na próxima consulta', 'Informe o seu médico ou enfermeiro', 'Ligue para a clínica no mesmo dia', 'Contacte imediatamente o seu médico ou enfermeiro', 'Vá ao hospital imediatamente'),
    'de': ('Notieren Sie es und besprechen Sie es beim nächsten Termin', 'Informieren Sie Ihren Arzt oder das Pflegepersonal', 'Rufen Sie die Klinik noch am selben Tag an', 'Kontaktieren Sie sofort Ihren Arzt oder das Pflegepersonal', 'Gehen Sie sofort ins Krankenhaus'),
    'fr': ('Notez-le et parlez-en lors de votre prochaine consultation', 'Informez votre médecin ou le personnel infirmier', 'Appelez la clinique le jour même', 'Contactez immédiatement votre médecin ou le personnel infirmier', 'Rendez-vous immédiatement à l’hôpital'),
    'it': ('Prenda nota e ne parli alla prossima visita', 'Informi il medico o il personale infermieristico', 'Chiami la clinica lo stesso giorno', 'Contatti subito il medico o il personale infermieristico', 'Si rechi subito in ospedale'),
    'da': ('Notér det, og tal om det ved næste besøg', 'Fortæl din læge eller sygeplejerske om det', 'Ring til klinikken samme dag', 'Kontakt straks din læge eller sygeplejerske', 'Tag straks på hospitalet'),
    'sv': ('Anteckna det och ta upp det vid nästa besök', 'Berätta för din läkare eller sjuksköterska', 'Ring kliniken samma dag', 'Kontakta din läkare eller sjuksköterska omedelbart', 'Åk till sjukhuset omedelbart'),
    'nb': ('Noter det og ta det opp ved neste besøk', 'Gi beskjed til legen eller sykepleieren', 'Ring klinikken samme dag', 'Kontakt legen eller sykepleieren umiddelbart', 'Dra til sykehuset umiddelbart'),
    'fi': ('Kirjaa asia muistiin ja keskustele siitä seuraavalla käynnillä', 'Kerro lääkärille tai hoitajalle', 'Soita klinikalle samana päivänä', 'Ota heti yhteyttä lääkäriin tai hoitajaan', 'Mene heti sairaalaan'),
}


def messages_for(locale):
    return {source: native for aliases, native in zip(SOURCES, HEADINGS[locale], strict=True)
            for source in aliases}
