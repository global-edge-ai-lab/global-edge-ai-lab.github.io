# Global Edge AI Lab website

Official static website for the Global Edge AI Lab at LUMS. Plain HTML, CSS and JavaScript; no dependencies or build step.

## Repository layout

```text
website/            Three public pages and optimized images
scripts/            Dependency-free site validation
.github/workflows/  Validation and GitHub Pages deployment
```

Only `website/` is uploaded to GitHub Pages.

## Preview and validate

From the repository root:

```bash
python3 scripts/validate_site.py
python3 -m http.server 8000 --directory website
```

Open http://localhost:8000. Edit files in `website/` directly. Do not put credentials or internal documents in that directory.

## Team review

Keep the repository private during review. Team members with repository access can clone it and run the preview command above. Validation runs on pushes and pull requests; deployment is skipped while the repository is private.

## Publish on 1 December 2026

1. Under **Settings → General → Danger Zone**, change repository visibility to **Public**.
2. Under **Settings → Pages → Build and deployment**, select **GitHub Actions**.
3. Under **Actions → Validate and deploy website**, select **Run workflow** on `main`.

After launch, pushes to `main` validate and deploy automatically. Pull requests validate without publishing. Changing visibility alone does not publish the website, and no scheduled visibility change is configured.

Configure the custom domain and HTTPS in the repository's Pages settings.
