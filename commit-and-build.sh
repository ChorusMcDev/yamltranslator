#!/bin/bash

# Script to commit changes and trigger automated build

echo "🚀 Preparing to commit and trigger automated build..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository. Please initialize git first:"
    echo "   git init"
    echo "   git remote add origin https://github.com/ChorusMcDev/yamltranslator.git"
    exit 1
fi

# Check git status
echo "📋 Current git status:"
git status --short

echo ""
echo "📝 Files to be committed:"
echo "   • .github/workflows/build-and-release.yml (new CI/CD workflow)"
echo "   • src/version.py (new version management)"
echo "   • version_info.py (Windows version info)"
echo "   • YAMLTranslator.spec (updated with version support)"
echo "   • src/main.py (updated with version display and CLI args)"
echo "   • README.md (updated with build documentation)"

echo ""
read -p "❓ Do you want to commit these changes and trigger a build? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "✅ Committing changes..."
    
    # Add all the new and modified files
    git add .github/workflows/build-and-release.yml
    git add src/version.py
    git add version_info.py
    git add YAMLTranslator.spec
    git add src/main.py
    git add README.md
    
    # Commit with a descriptive message
    git commit -m "🚀 Add automated CI/CD pipeline with cross-platform builds

- Add GitHub Actions workflow for automated builds
- Support Windows x64 and Linux x64 platforms
- Automatic version numbering (1.0.1-{build_number})
- Pre-release publishing with executable attachments
- Version management system with CLI support
- Automatic cleanup of old pre-releases
- Updated documentation with build information"

    echo "✅ Changes committed successfully!"
    echo ""
    echo "🔄 Pushing to GitHub to trigger automated build..."
    
    # Push to trigger the workflow
    git push origin main
    
    echo "✅ Push completed!"
    echo ""
    echo "🎉 Automated build should start shortly. You can monitor progress at:"
    echo "   https://github.com/ChorusMcDev/yamltranslator/actions"
    echo ""
    echo "📦 Once complete, pre-release will be available at:"
    echo "   https://github.com/ChorusMcDev/yamltranslator/releases"
    
else
    echo "❌ Commit cancelled."
    echo "💡 You can review changes with: git diff"
fi
