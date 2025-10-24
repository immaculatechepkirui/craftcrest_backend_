# Allow patching of uploaded images — README entry

Summary
-------
I updated the serializers and suggested view changes so uploaded images can be patched (updated or appended) without forcing clients to re-upload everything. Previously, the API blocked any image changes because image upload fields were write-only/required in ways that prevented PATCH/partial updates. The changes make image uploads flexible for both creating a resource (still enforcing minimums where required) and for patching/updating images later.

What I changed (high level)
---------------------------
- Made multipart image upload fields optional for partial updates (removed `required=True` on list image fields).
- Enforced "min number of images" only on create, not on PATCH.
- Added an `update()` implementation to the portfolio serializer so PATCH can append new images.
- Kept `PortfolioImageSerializer` writable so a client can PATCH a single image resource (replace the file).
- Recommended view changes: enable `MultiPartParser`/`FormParser` for endpoints that accept files.
- Suggested a small dedicated "image-only" user endpoint/serializer for updating user profile images safely.

Why this approach
-----------------
- PATCH/partial updates must not require fields that are only needed at creation. Making file-lists optional prevents validation errors when a client wants to update only the title or add one image.
- Appending new images through the portfolio serializer is convenient for clients who want to add images in batches.
- Allowing detail-level updates of `PortfolioImage` objects (PATCH /portfolio-images/<id>/) provides a clean way to replace a specific image without touching the portfolio.
- Using `MultiPartParser` and `FormParser` ensures DRF correctly reads uploaded files from multipart/form-data requests.

2) Views: accept multipart/form-data
- Ensure endpoints that accept file uploads use DRF parsers:


3) Example usage (curl)
- Append images to an existing portfolio (PATCH, multipart):

- Replace a single portfolio image (PATCH to portfolio-image detail):

Notes and recommendations
-------------------------
- Client must use multipart/form-data for any request that uploads files (browsers or mobile SDKs will do this automatically when sending files).
- If you want to allow replacing an image through the portfolio nested payload (e.g., submit {"images": [{"id": 5, "image": <file>}]}) we can implement nested writable logic, but I recommend keeping replace operations on the PortfolioImage detail endpoint — it's simpler and safer.
- If you need "atomic replace and delete" semantics (replace file and delete old file from storage), ensure your storage backend removes or overwrites files as appropriate (Django default FileField behavior simply replaces the DB reference; if you need to delete old files from storage you should delete them in the model save/delete signal).
- Tests: add tests for:
  - Create portfolio with >=10 images
  - Patch portfolio adding 1+ images
  - Patch portfolio title without sending images (should succeed)
  - Patch PortfolioImage detail to replace file

What I did, and what's next
---------------------------
I updated the serializers to allow partial updates and added an update implementation that appends files so PATCH can be used to add images. I also made sure the single-image serializer is writable so clients can replace one image via the portfolio-image detail endpoint. Next, please add the parser changes to the viewsets (MultiPartParser/FormParser) and deploy tests covering create and patch use-cases. If you'd like, I can produce the exact patch/diff for your repo (serializers + views + example tests) — paste the repository path or permit me to open the files and I'll prepare the PR-ready changes.
