# Global Edge AI Lab website

Official static website for the Global Edge AI Lab at LUMS. Plain HTML, CSS and JavaScript; no dependencies or build step.

## Repository layout

```text
website/            Five public pages and optimized images
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

## Deployment

The website is live at **https://globaledgeailab.com/**. This repository is public and GitHub Pages uses the **GitHub Actions** publishing source.

Pushes to `main` validate and deploy `website/` automatically. Pull requests validate without publishing. To redeploy manually, open **Actions → Validate and deploy website → Run workflow** on `main`.

For review, create a branch or pull request and run the local preview command above. Revert a commit on `main` to roll back a website change. Deployment is skipped if the repository is made private.

## Custom domain

The production domain is `globaledgeailab.com`; `www.globaledgeailab.com` should redirect to it. The `website/CNAME` file records this choice, but an Actions deployment also requires setting the domain in **Settings → Pages → Custom domain**.

Before launch, an organization owner can verify `globaledgeailab.com` under the **organization's Settings → Pages** using GitHub's generated TXT record. Keep that TXT record permanently.

After Pages is enabled and the initial deployment succeeds:

1. Set `globaledgeailab.com` as the custom domain in the repository's Pages settings.
2. Replace the GoDaddy parked `A` record with four `A` records for `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, and `185.199.111.153`.
3. Change the `www` CNAME target to `global-edge-ai-lab.github.io`. Preserve other DNS records.
4. Wait for GitHub's DNS check and HTTPS certificate, then enable **Enforce HTTPS**.
5. Verify the bare domain, the `www` redirect, and all five pages over HTTPS.
