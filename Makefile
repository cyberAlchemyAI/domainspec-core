# Submodule discipline helpers — see SUBMODULE-DISCIPLINE.md
.PHONY: bootstrap config status sync bump-check doctor help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  %-12s %s\n", $$1, $$2}'

bootstrap: ## First-time setup after clone (init recursive + config)
	git submodule update --init --recursive
	$(MAKE) config

config: ## Set repo-standard submodule git config (per clone, local)
	git config submodule.recurse true
	git config status.submoduleSummary true
	git config diff.submodule log
	git config push.recurseSubmodules check
	@echo "submodule config set."

status: ## Show submodule drift vs recorded pointers
	git submodule status --recursive
	@echo "---"
	git status --short

sync: ## Pull each submodule to the tip of its tracked branch
	git submodule update --remote --recursive
	@echo "Submodules moved to their tracked-branch tips. Review, then 'make bump-check'."

bump-check: ## Verify submodule commits are pushed before bumping the parent
	@git push --recurse-submodules=check --dry-run >/dev/null 2>&1 \
		&& echo "OK: all referenced submodule commits are pushed; safe to commit + push the parent gitlink." \
		|| { echo "BLOCKED: unpushed submodule commits — push the submodule first."; exit 1; }

doctor: ## Diagnose detached HEADs / dirty submodules / orphaned gitlinks
	@echo "== branch / detached =="
	@git config -f .gitmodules --get-regexp path | awk '{print $$2}' | while read p; do \
		echo "  $$p: $$(git -C "$$p" symbolic-ref -q --short HEAD 2>/dev/null || echo DETACHED@$$(git -C "$$p" rev-parse --short HEAD 2>/dev/null))"; \
	done
	@echo "== dirty submodules =="
	@git config -f .gitmodules --get-regexp path | awk '{print $$2}' | while read p; do \
		test -z "$$(git -C "$$p" status --porcelain 2>/dev/null)" || echo "  $$p DIRTY"; \
	done
	@echo "== orphaned gitlinks (committed in tree, NOT declared in .gitmodules) =="
	@git ls-files -s | awk '$$1==160000{print $$4}' | while read p; do \
		git config -f .gitmodules --get-regexp path 2>/dev/null | awk '{print $$2}' | grep -qx "$$p" \
		|| echo "  ORPHAN: $$p"; \
	done
	@echo "(clean if nothing listed under dirty / orphan)"
