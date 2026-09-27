// Runtime-dependent finalization of the 38 native body pages before shell assembly.
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const [candidate,final,template]=process.argv.slice(2);
const skill=process.env.PRESENTATIONS_SKILL_DIR,python=process.env.RUNTIME_PYTHON;
if(!template||!skill||!python||!process.env.RUNTIME_NODE_MODULES)throw Error('Usage: node finalize_atlas_content.mjs candidate.pptx final.pptx official-template.pptx; set PRESENTATIONS_SKILL_DIR, RUNTIME_PYTHON and RUNTIME_NODE_MODULES.');
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const workspace=path.resolve(path.dirname(final),'..');
const tables=[5,24,29,35,37];
const result=await finalizePresentation({
 workspaceDir:workspace,candidatePath:path.resolve(candidate),finalPath:path.resolve(final),pythonExecutable:python,
 integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
 layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
 layoutArgs:['--expected-slide-size-emu','12196763,6858000','--validate-heading-fit',...tables.flatMap(n=>['--require-native-table-slide',String(n)])],
 explicitTotalSlideCount:38,requiredNativeChartOwnerSlides:[4,11,12,24,25,26],requiredNativeTableOwnerSlides:tables,
 materializeLiteralChartWorkbooks:true,
 fontPolicy:{basis:'reference',families:['Microsoft YaHei'],referencePath:path.resolve(template),referenceSha256:'c6f6cc8245ebec463396f1b35fe2700c34dc85edfd2836509cdbdd7e23f00127'},
 verifyArtifactToolImport:true,receiptPath:path.join(workspace,'receipts',path.basename(final)+'.validation.json'),
});
console.log(JSON.stringify({finalPath:result.finalPath,receiptPath:result.receiptPath,sha256:result.finalSha256}));
