// Canonical medication editing only; never infer drug IDs from free text.
function medicationEditorState(profile, catalog) {
  if (['medications','concomitant_drugs'].some(key => Object.hasOwn(profile,key)) ||
      ['concomitant_drugs','bleomycin_concomitant'].some(key => profile.findings && Object.hasOwn(profile.findings,key))) throw new Error('unsupported');
  const value=profile.concomitant_medications;
  if (value === undefined || value === null) return {status:'unknown',drug_ids:[]};
  const known=new Set(catalog.map(drug => drug.id));
  if (!value || typeof value !== 'object' || Array.isArray(value) ||
      Object.keys(value).length !== 2 || !Object.hasOwn(value,'status') || !Object.hasOwn(value,'drug_ids') ||
      !['unknown','partial','complete'].includes(value.status) || !Array.isArray(value.drug_ids) ||
      value.drug_ids.some(id => typeof id !== 'string' || !known.has(id)) ||
      new Set(value.drug_ids).size !== value.drug_ids.length || (value.status === 'unknown' && value.drug_ids.length)) throw new Error('invalid');
  return {status:value.status,drug_ids:[...value.drug_ids]};
}
function medicationEditorUpdate(profile, status, drugIds, catalog) {
  medicationEditorState(profile,catalog); // Refuse to overwrite unsupported existing data.
  const next={...profile,concomitant_medications:{status,drug_ids:[...drugIds]}};
  medicationEditorState(next,catalog);
  return next;
}
function closeMedicationEditors() {
  document.querySelectorAll('.medication-editor').forEach(panel => { panel.open=false; });
}
function installMedicationEditor(editorMode, host) {
  const copy=medicationEditorConfig.copy, catalog=medicationEditorConfig.drugs;
  const panel=document.createElement('details');panel.className='quest-group medication-editor';panel.id=editorMode === 'form' ? 'formMedicationEditor' : 'medicationEditor';
  panel.style.cssText='margin-top:16px;padding:16px;border:1px solid #c5d8cf;border-radius:12px;background:#f4f8f6';
  const summary=document.createElement('summary');summary.textContent=editorMode === 'form' ? copy.formTitle : copy.title;summary.style.cssText='cursor:pointer;font-weight:700';panel.appendChild(summary);
  const note=document.createElement('p');note.textContent=copy.notice;panel.appendChild(note);
  const statusLabel=document.createElement('label');statusLabel.className='qt-label';statusLabel.textContent=copy.status;
  const status=document.createElement('select');status.id=editorMode+'MedicationStatus';statusLabel.appendChild(status);
  for (const key of ['unknown','partial','complete']) {const option=document.createElement('option');option.value=key;option.textContent=copy[key];status.appendChild(option);}
  panel.appendChild(statusLabel);
  const drugLabel=document.createElement('label');drugLabel.className='qt-label';drugLabel.textContent=copy.drugs;
  const drugs=document.createElement('select');drugs.id=editorMode+'MedicationDrugs';drugs.multiple=true;drugs.size=8;drugs.style.width='100%';drugLabel.appendChild(drugs);
  for (const drug of catalog) {const option=document.createElement('option');option.value=drug.id;option.textContent=drug.name+' · '+drug.id;drugs.appendChild(option);}
  panel.appendChild(drugLabel);
  const help=document.createElement('p');help.textContent=copy.selectHelp;panel.appendChild(help);
  const apply=document.createElement('button');apply.type='button';apply.className='btn btn-secondary';apply.textContent=editorMode === 'form' ? copy.formApply : copy.apply;panel.appendChild(apply);
  const message=document.createElement('p');message.setAttribute('role','status');message.setAttribute('aria-live','polite');panel.appendChild(message);
  let source=null, profile=null, sourceQuest=null;
  function exampleMedicationLocked(candidate) {
    const banner=document.getElementById('exampleLockBanner');
    return editorMode === 'form' && candidate && candidate.concomitant_medications != null && banner && !banner.hidden;
  }
  panel.addEventListener('toggle',() => {
    if (!panel.open) return;
    source=null;profile=null;apply.disabled=true;message.textContent='';
    if (mode !== editorMode || isInteractionLocked()) return;
    const candidate=buildProfile();
    if (!candidate) {message.textContent=editorMode === 'form' ? copy.formInvalid : copy.invalid;return;}
    if (exampleMedicationLocked(candidate)) {message.textContent=copy.formLocked;return;}
    try {
      const value=medicationEditorState(candidate,catalog);
      status.value=value.status;
      for (const option of drugs.options) option.selected=value.drug_ids.includes(option.value);
      source=editorMode === 'form' ? JSON.stringify(candidate) : textarea.value;sourceQuest=activeQuest;profile=candidate;apply.disabled=false;
    } catch (error) {message.textContent=editorMode === 'form' && error.message === 'invalid' ? copy.formInvalid : (copy[error.message] || copy.invalid);}
  });
  apply.addEventListener('click',() => {
    if (mode !== editorMode || isInteractionLocked()) return;
    const candidate=editorMode === 'form' ? buildProfile() : profile;
    if (editorMode === 'form' && !candidate) {message.textContent=copy.formInvalid;return;}
    if (exampleMedicationLocked(candidate)) {message.textContent=copy.formLocked;return;}
    const current=editorMode === 'form' ? JSON.stringify(candidate) : textarea.value;
    if (source === null || source !== current || (editorMode === 'form' && sourceQuest !== activeQuest)) {
      message.textContent=editorMode === 'form' ? copy.formChanged : copy.changed;return;
    }
    try {
      const next=medicationEditorUpdate(candidate,status.value,Array.from(drugs.selectedOptions,option=>option.value),catalog);
      // The full form base already participates in assembly, JSON transfer and
      // draft persistence. Do not invent a second medicine state or drop fields.
      if (editorMode === 'form') formProfileBase=next;
      else textarea.value=JSON.stringify(next,null,2);
      source=editorMode === 'form' ? JSON.stringify(next) : textarea.value;profile=next;
      setError('');markPlanDirty();saveDraft();updateRunBtnEnabled();updateImpactPanelLocal();
      message.textContent=editorMode === 'form' ? copy.formSaved : copy.saved;
    } catch (error) {message.textContent=editorMode === 'form' && error.message === 'invalid' ? copy.formInvalid : (copy[error.message] || copy.invalid);}
  });
  host.appendChild(panel);
}
installMedicationEditor('json',jsonPane);
installMedicationEditor('form',formPane);
modeFormBtn.addEventListener('click',closeMedicationEditors);
modeJsonBtn.addEventListener('click',closeMedicationEditors);
personalizeBtn && personalizeBtn.addEventListener('click',closeMedicationEditors);
