#!/usr/bin/env bash
# Colores para output

export RED='\033[0;31m'
export GREEN='\033[0;32m'
export YELLOW='\033[1;33m'
export BLUE='\033[0;34m'
export CYAN='\033[0;36m'
export MAGENTA='\033[0;35m'
export NC='\033[0m' # No Color

# Desactivar colores si estamos en CI
if [ -n "$CI" ]; then
    export RED=''
    export GREEN=''
    export YELLOW=''
    export BLUE=''
    export CYAN=''
    export MAGENTA=''
    export NC=''
fi
