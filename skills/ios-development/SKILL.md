---
name: ios-development
description: Apply pragmatic Swift and iOS implementation and review guidance. Use for SwiftUI or UIKit screens, concurrency, persistence, navigation, packages, Xcode projects, platform availability, builds, and tests.
---

# Develop for iOS

1. Load project policy and inspect deployment target, Swift version, SwiftUI/UIKit,
   project or workspace, scheme, package structure, architecture, persistence,
   and build/test commands before assumptions.
2. Follow existing state, dependency, navigation, and concurrency patterns. Check
   API availability against the actual deployment target.
3. Keep SwiftUI views focused and move substantial non-view behavior out of large
   bodies. Respect actor isolation, cancellation, ownership, and UI-thread rules.
4. Treat persistence migrations, sync semantics, authentication, entitlements,
   privacy, and destructive state changes as high risk.
5. Add proportionate unit/UI coverage using the project's testing style. Run the
   configured canonical check; rigorous projects always provide `commands.check`.
6. Do not impose MVVM, coordinators, repositories, clean architecture, or a
   wholesale project-file rewrite without project evidence.

