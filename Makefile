build-all:
	bash ./scripts/build.sh

test-all:
	bash ./scripts/test.sh

coverage-all:
	bash ./scripts/coverage.sh

check-imports:
	bash ./scripts/check_imports.sh

generate-new-pdf-samples:
	bash ./scripts/new_pdf_samples.sh

compare-pdf-diffs:
	bash ./scripts/pdf_diffs.sh

deploy:
	bash ./scripts/create_release.sh
