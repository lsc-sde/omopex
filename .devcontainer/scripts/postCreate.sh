cd /home/vscode/ssl-certificates && ./apply_certificates.sh
git config --global --add safe.directory /workspaces/omop_projects
git config --global init.defaultBranch main
cd /workspaces/omop_projects
pre-commit install

cat >> ~/.inputrc <<'EOF'
"\e[A": history-search-backward
"\e[B": history-search-forward
EOF
