---
description: 
globs: 
alwaysApply: true
---

# Your rule content

- You can @ files here
- You can use markdown but dont have to

- when developing a front page, cut out the components in blocks. 
- Components should be located in the “components” folder and structured according to where they are displayed (for example: if you're making a page that's in lab, you'll make components in the “components/lab” folder).
- Check whether a component exists for the requirement. If a page already exists, but some of the details don't fit, adapt the component to make it more generic in terms of code.
- HTTP and other requests are made in the blinds.
-If a page is intended to be referenced on Google, the css must be in the style tag and not in the classes of the template part, in order to improve SEO.
-for a page not intended to be referenced, use tailwind in the classes in the template section


-respects SOLID development rules: 
-don't repeat yourself (DRY)
-keep it simple
-Single Responsibility Principle (SRP)
-Open/Closed Principle: open to evolution, closed to modification
-Interface Segregation Principle (ISP)
-Dependency Inversion Principle (DIP)

-code must be in English, comments in French
-names of variables, functions and classes must be understandable in relation to their context
-when choosing between js and ts, always favor typscript and strong typing
-A function must have a responsibility: find the right balance between a function with a single responsibility and simplicity in calling up the function.

-ask questions to make sure you'll be able to meet the need as best you can