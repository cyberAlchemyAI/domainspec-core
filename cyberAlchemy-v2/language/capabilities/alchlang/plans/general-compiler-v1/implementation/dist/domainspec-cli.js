import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
export const DOMAINSPEC_PACKAGE = "@domainspec-v2/cli";
export const DOMAINSPEC_VERSION = "1.0.0";
export function defaultDomainSpecPackageRoot() {
    return process.env.ALCHLANG_DOMAINSPEC_PACKAGE_ROOT ?? path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../../../../../../../projects/domainspec-v2/impl/cli");
}
export async function loadDomainSpecCompiler(packageRoot = defaultDomainSpecPackageRoot()) {
    const root = path.resolve(packageRoot);
    const packageBytes = readFileSync(path.join(root, "package.json"));
    const manifest = JSON.parse(packageBytes.toString("utf8"));
    if (manifest.name !== DOMAINSPEC_PACKAGE || manifest.version !== DOMAINSPEC_VERSION) {
        throw new Error(`DOMAINSPEC_VERSION_MISMATCH: expected ${DOMAINSPEC_PACKAGE}@${DOMAINSPEC_VERSION}; got ${manifest.name}@${manifest.version}`);
    }
    const entry = manifest.exports?.["."]?.import;
    if (typeof entry !== "string" || !entry.startsWith("./") || path.relative(root, path.resolve(root, entry)).startsWith("..")) {
        throw new Error("DOMAINSPEC_PUBLIC_ENTRY_REQUIRED: package must export its public ESM entry");
    }
    const entryPath = path.resolve(root, entry);
    let entryBytes;
    try {
        entryBytes = readFileSync(entryPath);
    }
    catch {
        throw new Error(`DOMAINSPEC_BUILD_REQUIRED: build ${root} before using AlchLang`);
    }
    const api = await import(pathToFileURL(entryPath).href);
    if (api.CLI_PACKAGE_NAME !== DOMAINSPEC_PACKAGE || api.CLI_VERSION !== DOMAINSPEC_VERSION || typeof api.compileProject !== "function" || typeof api.runCli !== "function") {
        throw new Error(`DOMAINSPEC_BUILD_MISMATCH: rebuild ${DOMAINSPEC_PACKAGE}@${DOMAINSPEC_VERSION}; manifest and built public API disagree`);
    }
    let version = "";
    const versionCode = api.runCli(["--version"], { stdout(value) { version += value; }, stderr() { } });
    if (versionCode !== 0 || version.trim() !== DOMAINSPEC_VERSION)
        throw new Error("DOMAINSPEC_BUILD_MISMATCH: CLI version does not match public API");
    const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
    const requireLayout = () => { if (api.APPLICATION_LAYOUT?.id !== "domainspec.application-layout/v1" || !api.APPLICATION_PATHS || typeof api.outputImport !== "function")
        throw Error("DOMAINSPEC_APPLICATION_LAYOUT_BUILD_REQUIRED"); };
    return {
        compileEventBindings(value, language) {
            if (typeof api.compileSystemIntegrationManifest !== "function" || typeof api.renderSystemIntegrationContract !== "function")
                throw Error("DOMAINSPEC_MESSAGE_BUILD_REQUIRED");
            const manifest = api.compileSystemIntegrationManifest(value, language);
            return { manifest, source: api.renderSystemIntegrationContract(manifest) };
        },
        get applicationPaths() {
            if (api.APPLICATION_LAYOUT?.id !== "domainspec.application-layout/v1" || !api.APPLICATION_PATHS || typeof api.outputImport !== "function")
                throw Error("DOMAINSPEC_APPLICATION_LAYOUT_BUILD_REQUIRED");
            return api.APPLICATION_PATHS;
        },
        get applicationLayoutId() { requireLayout(); return api.APPLICATION_LAYOUT.id; },
        outputImport(from, to) { requireLayout(); return api.outputImport(from, to); },
        supportsExactUInt64: api.EXACT_UINT64_PROFILE === "domainspec.typescript-exact-uint64/v1",
        compileDeclarativeFunction(value) {
            if (api.DECLARATIVE_FUNCTION_PROFILE !== "domainspec.declarative-function/v1" || typeof api.compileDeclarativeFunction !== "function")
                throw Error("DOMAINSPEC_DECLARATIVE_BUILD_REQUIRED");
            return api.compileDeclarativeFunction(value);
        },
        binding: { package: DOMAINSPEC_PACKAGE, version: DOMAINSPEC_VERSION, package_root: root, package_sha256: sha256(packageBytes), entry_sha256: sha256(entryBytes) },
        compileProject(sourceRoot) {
            const result = api.compileProject(path.resolve(sourceRoot));
            if (result.certificate?.compiler?.package !== DOMAINSPEC_PACKAGE || result.certificate?.compiler?.version !== DOMAINSPEC_VERSION || result.certificate?.authority_effect !== "none" || result.graph?.authority_effect !== "none") {
                throw new Error("DOMAINSPEC_CERTIFICATE_MISMATCH: compilation is not bound to the selected compiler");
            }
            return result;
        },
        runCli(args, io) { return api.runCli(args, io); },
    };
}
// Deliberately excludes experimental execution, source authoring and deployment recipes.
const COMPILER_COMMANDS = new Set(["--version", "--help", "capabilities", "doctor", "lint", "receipt", "compile", "build", "verify", "instantiate", "instantiate-project", "verify-project", "formalize", "formalize-check", "certify", "certify-check"]);
export async function runDomainSpecCli(args, io, packageRoot) {
    const command = args[0] ?? "--help";
    if (!COMPILER_COMMANDS.has(command))
        throw new Error(`DOMAINSPEC_COMMAND_UNSUPPORTED:${command}`);
    const compiler = await loadDomainSpecCompiler(packageRoot);
    return compiler.runCli(args.length ? args : ["--help"], io);
}
