import {readFileSync,mkdirSync,existsSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
const archive='../domainspec-v2/development/evolvable-validation-framework/distribution/portable-audit-v4/artifacts/evf-audit-kit-0.4.0-linux-x86_64.tar.gz';
const expected='748b1afcd27ae52b9c1f105a97314cf05a6582aaed4048b6a4a48a28fe4fca08';
if(createHash('sha256').update(readFileSync(archive)).digest('hex')!==expected)throw Error('EVF archive identity mismatch');
mkdirSync('.tools/evf',{recursive:true});
if(!existsSync('.tools/evf/evf-audit-kit-0.4.0'))execFileSync('tar',['-xzf',archive,'-C','.tools/evf']);
execFileSync('.tools/evf/evf-audit-kit-0.4.0/evf',['doctor'],{stdio:'inherit'});
