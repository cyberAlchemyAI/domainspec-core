# `@domainspec-v2/cli`

This directory contains the private candidate for the DomainSpec v2 stable
foundation CLI. Its supported command name is `domainspec-v2`; the candidate
eventually exposes only `lint <project-root>` and `receipt <project-root>`.

The package is not released, published, registered, deployed, or production
ready. The current source boundary exports only immutable package and contract
identity constants. The existing development CLI and factory commands remain
internal to `@domainspec-v2/impl`.

The supported target environment is Linux x64 with externally installed Node.js
`v24.19.0` and npm `11.17.0`. Declaring that environment does not prove that a
compiled candidate or clean-root build exists.
