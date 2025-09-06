# GitHub Actions Setup Guide

This guide explains how to configure GitHub repository settings to enable the automated CI/CD pipeline for demopy_gb_jj.

## 🔧 Repository Settings Configuration

### **Step 1: Configure Workflow Permissions**

1. **Go to Repository Settings**:
   - Navigate to `https://github.com/jj-devhub/demopy/settings`
   - Click on "Actions" in the left sidebar
   - Click on "General"

2. **Set Workflow Permissions**:
   - Under "Workflow permissions", select **"Read and write permissions"**
   - Check ✅ **"Allow GitHub Actions to create and approve pull requests"**
   - Click **"Save"**

### **Step 2: Configure Branch Protection (Optional but Recommended)**

1. **Go to Branch Settings**:
   - Navigate to `https://github.com/jj-devhub/demopy/settings/branches`
   - Click **"Add rule"** for the `main` branch

2. **Configure Protection Rules**:
   - ✅ **"Require status checks to pass before merging"**
   - ✅ **"Require branches to be up to date before merging"**
   - Select status checks: "Code Quality", "Automated Release Pipeline"
   - ✅ **"Include administrators"** (optional)
   - ❌ **"Restrict pushes that create files"** (leave unchecked for automation)

3. **Allow Automation**:
   - ✅ **"Allow force pushes"** → **"Specify who can force push"** → Add `github-actions[bot]`
   - Or alternatively, don't enable force push restrictions

### **Step 3: Configure Secrets (If Using Personal Access Token)**

If you prefer using a Personal Access Token instead of GITHUB_TOKEN:

1. **Create Personal Access Token**:
   - Go to `https://github.com/settings/tokens`
   - Click **"Generate new token (classic)"**
   - Select scopes:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `workflow` (Update GitHub Action workflows)
     - ✅ `write:packages` (Upload packages to GitHub Package Registry)

2. **Add Token to Repository Secrets**:
   - Go to `https://github.com/jj-devhub/demopy/settings/secrets/actions`
   - Click **"New repository secret"**
   - Name: `PERSONAL_ACCESS_TOKEN`
   - Value: Your generated token

3. **Update Workflow** (if using PAT):
   ```yaml
   - uses: actions/checkout@v4
     with:
       token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
   ```

## 🔍 Troubleshooting Common Issues

### **Issue 1: "Permission denied" Error**

**Symptoms:**
```
remote: Permission to jj-devhub/demopy.git denied to github-actions[bot]
fatal: unable to access 'https://github.com/jj-devhub/demopy.git/': The requested URL returned error: 403
```

**Solutions:**
1. ✅ Verify workflow permissions are set to "Read and write"
2. ✅ Check that branch protection allows automation
3. ✅ Ensure GITHUB_TOKEN has proper scopes
4. ✅ Verify git configuration uses correct authentication

### **Issue 2: "Resource not accessible by integration" Error**

**Symptoms:**
```
Resource not accessible by integration
```

**Solutions:**
1. ✅ Add explicit permissions to workflow file:
   ```yaml
   permissions:
     contents: write
     actions: write
   ```
2. ✅ Check repository settings allow workflow permissions

### **Issue 3: Infinite Loop Prevention**

**Symptoms:**
- Workflow triggers itself repeatedly
- Multiple version bump commits

**Solutions:**
1. ✅ Use `[skip ci]` in commit messages:
   ```yaml
   git commit -m "chore: bump version to X.Y.Z [skip ci]"
   ```
2. ✅ Add path exclusions to workflow triggers:
   ```yaml
   on:
     push:
       paths-ignore:
         - 'version-bump-commits'
   ```

### **Issue 4: Tag Already Exists**

**Symptoms:**
```
fatal: tag 'v1.0.0' already exists
```

**Solutions:**
1. ✅ Check for existing tags before creation
2. ✅ Use conditional tag creation in workflow
3. ✅ Implement tag cleanup if needed

## 🔐 Security Best Practices

### **GITHUB_TOKEN vs Personal Access Token**

| Aspect | GITHUB_TOKEN | Personal Access Token |
|--------|--------------|----------------------|
| **Scope** | Repository-specific | User-wide access |
| **Lifetime** | Per workflow run | Until manually revoked |
| **Security** | Automatically managed | Manually managed |
| **Permissions** | Limited by workflow | Full user permissions |
| **Recommendation** | ✅ Preferred for most cases | Use only if GITHUB_TOKEN insufficient |

### **Recommended Approach:**
1. **Start with GITHUB_TOKEN** with proper permissions
2. **Use Personal Access Token** only if GITHUB_TOKEN limitations prevent functionality
3. **Regularly rotate** Personal Access Tokens if used
4. **Use fine-grained tokens** when available

## 📋 Verification Checklist

After configuration, verify the setup:

- [ ] Repository workflow permissions set to "Read and write"
- [ ] Branch protection configured (if desired)
- [ ] Workflow file has proper permissions block
- [ ] Git configuration uses correct authentication
- [ ] Test workflow runs successfully
- [ ] Version bump commits are created and pushed
- [ ] Git tags are created and pushed
- [ ] No infinite loops occur

## 🚀 Testing the Configuration

### **Manual Test:**
1. Make a small change to the repository
2. Commit with semantic message: `feat: test automated pipeline`
3. Push to main branch
4. Monitor GitHub Actions for successful execution

### **Expected Behavior:**
1. ✅ Workflow triggers automatically
2. ✅ Version analysis completes
3. ✅ Version files are updated
4. ✅ Commit is created and pushed
5. ✅ Git tag is created and pushed
6. ✅ Release workflow triggers
7. ✅ Package is built and published

## 📞 Getting Help

If you encounter issues:

1. **Check GitHub Actions logs** for detailed error messages
2. **Review repository settings** against this guide
3. **Test with minimal changes** to isolate issues
4. **Check GitHub Status** for platform-wide issues
5. **Consult GitHub Documentation** for latest updates

## 🔄 Maintenance

### **Regular Tasks:**
- [ ] Review and rotate Personal Access Tokens (if used)
- [ ] Update workflow permissions as needed
- [ ] Monitor for GitHub Actions platform updates
- [ ] Test automation periodically

### **When to Update:**
- GitHub Actions introduces new permission models
- Repository structure changes significantly
- Security requirements change
- Workflow complexity increases

---

**This configuration enables fully automated CI/CD with proper security and reliability!** 🎉
