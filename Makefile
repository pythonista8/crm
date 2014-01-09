SHELL := /bin/sh

.PHONY: deploy

deploy:
	bash -l -c "cd /var/www/crm; source ../env_crm/bin/activate; ./deploy.sh"
