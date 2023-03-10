# dbt-tutorial-course

Welcome to my course!

This repository (repo) contains the structure you'll need to get started on the dbt course (link here).

---

## The structure
This repo has 3 main areas:
1. **The top level** - everything you can see without clicking into a folder. This contains things that are used both in the model answers and in your lessons - such as the python packages you'll need and VSCode configuration.

2. **The answers folder**. This is how your project should look like at the end of the course. Feel free to use this for reference throughout the lessons if you're stuck, but remember - this will contain the final versions of everything so it may be several lessons ahead!

3. **The your_project folder**. This is blank as it's meant to be for all of your working!

---
## A note on forking vs. cloning
> **Don't clone this repo, fork it!**

Cloning the repo means that if you want to save your changes locally and push them remotely (to GitHub), it will attempt to overwrite the repo itself (the master branch) - or, you'll have to create your own version of code (a developer branch).

Both of these would clutter up this repo, instead - you should [fork the repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo).

Forking the repo means that you get your own copy of this repository, can makes changes locally, and push them to your own master branch.

Your (forked) repo should have an untouched `/answers` folder, and use the `/your_project` folder for all of your work when following along with the course.

### What if I need to rebase?

If I update this repository, and you want to rebase (update) your forked repository with my changes, then you'll need to do the following in VSCode:
1. Change onto your "main" branch, and make sure you don't have any pending changes (commits)
2. Run `git remote add upstream https://github.com/jack-cook-repo/dbt-tutorial-course.git`, this will point your local repository at this one and call it "upstream"
3. Run `git rebase upstream/main`, this will bring any changes from my repository into your local repository
4. Run `git push origin main --force`, this will update your "main" branch on GitHub with your local changes

So in summary, this process copies changes from this repository to your local repository, then pushes those changes to your forked repository on GitHub

https://medium.com/@topspinj/how-to-git-rebase-into-a-forked-repo-c9f05e821c8a

https://console.cloud.google.com/storage/browser/thelook_ecommerce_backup
