Cashflow
# 💰 CashFlow

Aplicación web para gestionar ingresos y gastos personales.  
Desarrollada con **Django REST Framework + Tailwind/React + PostgreSQL**.

# 📂 Mapa de documentación

La documentación inicial se encuentra organizada en la carpeta docs/ y las decisiones arquitectónicas en adr/.

    docs/01-vision-alcance.md → Acta de visión y alcance.

    docs/02-nfrs.md → Catálogo de requerimientos no funcionales.

    docs/03-c4-contexto-contenedores.md → Diseño C4 (contexto y contenedores).

    docs/04-backlog.md → Backlog inicial con historias INVEST.

    adr/ADR-000-monolito-django-postgres.md → Decisión arquitectónica inicial.

## 🗂️ Estructura de carpetas
```
├── adr
├── backend
│   └── __pycache__
├── core
│   ├── migrations
│   │   └── __pycache__
│   └── __pycache__
├── docs
├── node_modules
│   ├── @alloc
│   │   └── quick-lru
│   ├── ansi-regex
│   ├── ansi-styles
│   ├── anymatch
│   ├── any-promise
│   │   └── register
│   ├── arg
│   ├── autoprefixer
│   │   ├── bin
│   │   ├── data
│   │   └── lib
│   │       └── hacks
│   ├── balanced-match
│   ├── baseline-browser-mapping
│   │   └── dist
│   ├── binary-extensions
│   ├── brace-expansion
│   ├── braces
│   │   └── lib
│   ├── browserslist
│   ├── camelcase
│   ├── camelcase-css
│   ├── caniuse-lite
│   │   ├── data
│   │   │   ├── features
│   │   │   └── regions
│   │   └── dist
│   │       ├── lib
│   │       └── unpacker
│   ├── chokidar
│   │   ├── lib
│   │   └── types
│   ├── chokidar-cli
│   ├── cliui
│   ├── color-convert
│   ├── color-name
│   ├── commander
│   │   └── typings
│   ├── cross-spawn
│   │   └── lib
│   │       └── util
│   ├── cssesc
│   │   ├── bin
│   │   └── man
│   ├── decamelize
│   ├── dependency-graph
│   │   ├── lib
│   │   └── specs
│   ├── didyoumean
│   ├── dlv
│   │   └── dist
│   ├── eastasianwidth
│   ├── electron-to-chromium
│   ├── emoji-regex
│   │   └── es2015
│   ├── escalade
│   │   ├── dist
│   │   └── sync
│   ├── fast-glob
│   │   └── out
│   │       ├── managers
│   │       ├── providers
│   │       │   ├── filters
│   │       │   ├── matchers
│   │       │   └── transformers
│   │       ├── readers
│   │       ├── types
│   │       └── utils
│   ├── fastq
│   │   └── test
│   ├── fill-range
│   ├── find-up
│   ├── foreground-child
│   │   └── dist
│   │       ├── commonjs
│   │       └── esm
│   ├── fraction.js
│   │   ├── dist
│   │   ├── examples
│   │   ├── src
│   │   └── tests
│   ├── fs-extra
│   │   └── lib
│   │       ├── copy
│   │       ├── empty
│   │       ├── ensure
│   │       ├── fs
│   │       ├── json
│   │       ├── mkdirs
│   │       ├── move
│   │       ├── output-file
│   │       ├── path-exists
│   │       ├── remove
│   │       └── util
│   ├── function-bind
│   │   └── test
│   ├── get-caller-file
│   ├── glob
│   │   └── dist
│   │       ├── commonjs
│   │       └── esm
│   ├── glob-parent
│   ├── graceful-fs
│   ├── hasown
│   ├── @isaacs
│   │   └── cliui
│   │       ├── build
│   │       │   └── lib
│   │       └── node_modules
│   │           ├── ansi-regex
│   │           ├── ansi-styles
│   │           ├── emoji-regex
│   │           │   └── es2015
│   │           ├── string-width
│   │           ├── strip-ansi
│   │           └── wrap-ansi
│   ├── is-binary-path
│   ├── is-core-module
│   │   └── test
│   ├── isexe
│   │   └── test
│   ├── is-extglob
│   ├── is-fullwidth-code-point
│   ├── is-glob
│   ├── is-number
│   ├── jackspeak
│   │   └── dist
│   │       ├── commonjs
│   │       └── esm
│   ├── jiti
│   │   ├── dist
│   │   └── lib
│   ├── @jridgewell
│   │   ├── gen-mapping
│   │   │   ├── dist
│   │   │   │   └── types
│   │   │   ├── src
│   │   │   └── types
│   │   ├── resolve-uri
│   │   │   └── dist
│   │   │       └── types
│   │   ├── sourcemap-codec
│   │   │   ├── dist
│   │   │   ├── src
│   │   │   └── types
│   │   └── trace-mapping
│   │       ├── dist
│   │       ├── src
│   │       └── types
│   ├── jsonfile
│   ├── lilconfig
│   │   └── src
│   ├── lines-and-columns
│   │   └── build
│   ├── locate-path
│   ├── lodash.debounce
│   ├── lodash.throttle
│   ├── lru-cache
│   │   └── dist
│   │       ├── commonjs
│   │       └── esm
│   ├── merge2
│   ├── micromatch
│   ├── minimatch
│   │   └── dist
│   │       ├── commonjs
│   │       └── esm
│   ├── minipass
│   │   └── dist
│   │       ├── commonjs
│   │       └── esm
│   ├── mz
│   ├── nanoid
│   │   ├── async
│   │   ├── bin
│   │   ├── non-secure
│   │   └── url-alphabet
│   ├── @nodelib
│   │   ├── fs.scandir
│   │   │   └── out
│   │   │       ├── adapters
│   │   │       ├── providers
│   │   │       ├── types
│   │   │       └── utils
│   │   ├── fs.stat
│   │   │   └── out
│   │   │       ├── adapters
│   │   │       ├── providers
│   │   │       └── types
│   │   └── fs.walk
│   │       └── out
│   │           ├── providers
│   │           ├── readers
│   │           └── types
│   ├── node-releases
│   │   └── data
│   │       ├── processed
│   │       └── release-schedule
│   ├── normalize-path
│   ├── normalize-range
│   ├── object-assign
│   ├── object-hash
│   │   └── dist
│   ├── package-json-from-dist
│   │   └── dist
│   │       ├── commonjs
│   │       └── esm
│   ├── path-exists
│   ├── path-key
│   ├── path-parse
│   ├── path-scurry
│   │   └── dist
│   │       ├── commonjs
│   │       └── esm
│   ├── picocolors
│   ├── picomatch
│   │   └── lib
│   ├── pify
│   ├── pirates
│   │   └── lib
│   ├── @pkgjs
│   │   └── parseargs
│   │       ├── examples
│   │       └── internal
│   ├── p-limit
│   ├── p-locate
│   ├── postcss
│   │   └── lib
│   ├── postcss-cli
│   │   ├── lib
│   │   └── node_modules
│   │       ├── ansi-regex
│   │       ├── ansi-styles
│   │       ├── cliui
│   │       │   └── build
│   │       │       └── lib
│   │       ├── color-convert
│   │       ├── color-name
│   │       ├── emoji-regex
│   │       │   └── es2015
│   │       ├── is-fullwidth-code-point
│   │       ├── string-width
│   │       ├── strip-ansi
│   │       ├── wrap-ansi
│   │       ├── y18n
│   │       │   └── build
│   │       │       └── lib
│   │       │           └── platform-shims
│   │       ├── yargs
│   │       │   ├── build
│   │       │   │   └── lib
│   │       │   │       ├── typings
│   │       │   │       └── utils
│   │       │   ├── helpers
│   │       │   ├── lib
│   │       │   │   └── platform-shims
│   │       │   └── locales
│   │       └── yargs-parser
│   │           └── build
│   │               └── lib
│   ├── postcss-import
│   │   └── lib
│   ├── postcss-js
│   ├── postcss-load-config
│   │   └── src
│   ├── postcss-nested
│   ├── postcss-reporter
│   │   └── lib
│   ├── postcss-selector-parser
│   │   └── dist
│   │       ├── selectors
│   │       └── util
│   ├── postcss-value-parser
│   │   └── lib
│   ├── pretty-hrtime
│   ├── p-try
│   ├── queue-microtask
│   ├── read-cache
│   ├── readdirp
│   ├── require-directory
│   ├── require-main-filename
│   ├── resolve
│   │   ├── bin
│   │   ├── example
│   │   ├── lib
│   │   └── test
│   │       ├── dotdot
│   │       │   └── abc
│   │       ├── module_dir
│   │       │   ├── xmodules
│   │       │   │   └── aaa
│   │       │   ├── ymodules
│   │       │   │   └── aaa
│   │       │   └── zmodules
│   │       │       └── bbb
│   │       ├── node_path
│   │       │   ├── x
│   │       │   │   ├── aaa
│   │       │   │   └── ccc
│   │       │   └── y
│   │       │       ├── bbb
│   │       │       └── ccc
│   │       ├── pathfilter
│   │       │   └── deep_ref
│   │       ├── precedence
│   │       │   ├── aaa
│   │       │   └── bbb
│   │       ├── resolver
│   │       │   ├── baz
│   │       │   ├── browser_field
│   │       │   ├── dot_main
│   │       │   ├── dot_slash_main
│   │       │   ├── false_main
│   │       │   ├── incorrect_main
│   │       │   ├── invalid_main
│   │       │   ├── multirepo
│   │       │   │   └── packages
│   │       │   │       ├── package-a
│   │       │   │       └── package-b
│   │       │   ├── nested_symlinks
│   │       │   │   └── mylib
│   │       │   ├── other_path
│   │       │   │   └── lib
│   │       │   ├── quux
│   │       │   │   └── foo
│   │       │   ├── same_names
│   │       │   │   └── foo
│   │       │   ├── symlinked
│   │       │   │   ├── _
│   │       │   │   │   ├── node_modules
│   │       │   │   │   └── symlink_target
│   │       │   │   └── package
│   │       │   └── without_basedir
│   │       └── shadowed_core
│   │           └── node_modules
│   │               └── util
│   ├── reusify
│   │   └── benchmarks
│   ├── run-parallel
│   ├── set-blocking
│   ├── shebang-command
│   ├── shebang-regex
│   ├── signal-exit
│   │   └── dist
│   │       ├── cjs
│   │       └── mjs
│   ├── slash
│   ├── source-map-js
│   │   └── lib
│   ├── string-width
│   ├── string-width-cjs
│   │   └── node_modules
│   │       ├── ansi-regex
│   │       ├── emoji-regex
│   │       │   └── es2015
│   │       ├── is-fullwidth-code-point
│   │       └── strip-ansi
│   ├── strip-ansi
│   ├── strip-ansi-cjs
│   │   └── node_modules
│   │       └── ansi-regex
│   ├── sucrase
│   │   ├── bin
│   │   ├── dist
│   │   │   ├── esm
│   │   │   │   ├── parser
│   │   │   │   │   ├── plugins
│   │   │   │   │   │   └── jsx
│   │   │   │   │   ├── tokenizer
│   │   │   │   │   ├── traverser
│   │   │   │   │   └── util
│   │   │   │   ├── transformers
│   │   │   │   └── util
│   │   │   ├── parser
│   │   │   │   ├── plugins
│   │   │   │   │   └── jsx
│   │   │   │   ├── tokenizer
│   │   │   │   ├── traverser
│   │   │   │   └── util
│   │   │   ├── transformers
│   │   │   ├── types
│   │   │   │   ├── parser
│   │   │   │   │   ├── plugins
│   │   │   │   │   │   └── jsx
│   │   │   │   │   ├── tokenizer
│   │   │   │   │   ├── traverser
│   │   │   │   │   └── util
│   │   │   │   ├── transformers
│   │   │   │   └── util
│   │   │   └── util
│   │   ├── register
│   │   └── ts-node-plugin
│   ├── supports-preserve-symlinks-flag
│   │   └── test
│   ├── @tailwindcss
│   ├── tailwindcss
│   │   ├── lib
│   │   │   ├── cli
│   │   │   │   ├── build
│   │   │   │   ├── help
│   │   │   │   └── init
│   │   │   ├── css
│   │   │   ├── lib
│   │   │   ├── postcss-plugins
│   │   │   │   └── nesting
│   │   │   ├── public
│   │   │   ├── util
│   │   │   └── value-parser
│   │   ├── nesting
│   │   ├── node_modules
│   │   │   ├── glob-parent
│   │   │   └── jiti
│   │   │       ├── bin
│   │   │       ├── dist
│   │   │       │   └── plugins
│   │   │       └── lib
│   │   ├── peers
│   │   ├── scripts
│   │   ├── src
│   │   │   ├── cli
│   │   │   │   ├── build
│   │   │   │   ├── help
│   │   │   │   └── init
│   │   │   ├── css
│   │   │   ├── lib
│   │   │   ├── postcss-plugins
│   │   │   │   └── nesting
│   │   │   ├── public
│   │   │   ├── util
│   │   │   └── value-parser
│   │   ├── stubs
│   │   └── types
│   │       └── generated
│   ├── thenby
│   ├── thenify
│   ├── thenify-all
│   ├── tinyglobby
│   │   ├── dist
│   │   └── node_modules
│   │       ├── fdir
│   │       │   └── dist
│   │       └── picomatch
│   │           └── lib
│   ├── to-regex-range
│   ├── ts-interface-checker
│   │   └── dist
│   ├── universalify
│   ├── update-browserslist-db
│   ├── util-deprecate
│   ├── which
│   │   └── bin
│   ├── which-module
│   ├── wrap-ansi
│   ├── wrap-ansi-cjs
│   │   └── node_modules
│   │       ├── ansi-regex
│   │       ├── ansi-styles
│   │       ├── color-convert
│   │       ├── color-name
│   │       ├── emoji-regex
│   │       │   └── es2015
│   │       ├── is-fullwidth-code-point
│   │       ├── string-width
│   │       └── strip-ansi
│   ├── y18n
│   ├── yaml
│   │   ├── browser
│   │   │   └── dist
│   │   │       ├── compose
│   │   │       ├── doc
│   │   │       ├── nodes
│   │   │       ├── parse
│   │   │       ├── schema
│   │   │       │   ├── common
│   │   │       │   ├── core
│   │   │       │   ├── json
│   │   │       │   └── yaml-1.1
│   │   │       └── stringify
│   │   └── dist
│   │       ├── compose
│   │       ├── doc
│   │       ├── nodes
│   │       ├── parse
│   │       ├── schema
│   │       │   ├── common
│   │       │   ├── core
│   │       │   ├── json
│   │       │   └── yaml-1.1
│   │       └── stringify
│   ├── yargs
│   │   ├── lib
│   │   └── locales
│   └── yargs-parser
│       └── lib
├── static
│   ├── css
│   ├── icons
│   ├── js
│   └── src
└── templates
```


