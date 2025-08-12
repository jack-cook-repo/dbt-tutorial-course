# dbt-tutorial-course

Welcome to my course!

This repository (repo) contains the structure you'll need to get started on the dbt course ([link here](https://www.udemy.com/course/mastering-dbt-data-build-tool-bootcamp/?referralCode=FFF494163B7B9E5E846F)).

---

## The structure
This repo has 2 main areas:
1. **The top level** - everything you can see without clicking into a folder. This contains things that are used both in the model answers and in your lessons - such as the python packages you'll need and VSCode configuration.

2. **The answers folder**. This is how your project should look like at the end of the course. Feel free to use this for reference throughout the lessons if you're stuck, but remember - this will contain the final versions of everything so it may be several lessons ahead!

In the course, you'll be creating a 3rd area - `/lessons` - that will, by the end of the course, be (nearly) identical to the answers folder

---
## A note on forking vs. cloning
> **Don't clone this repo, fork it!**

Cloning the repo means that if you want to save your changes locally and push them remotely (to GitHub), it will attempt to overwrite the repo itself (the master branch) - or, you'll have to create your own version of code (a developer branch).

Both of these would clutter up this repo, instead - you should [fork the repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo).

Forking the repo means that you get your own copy of this repository, can makes changes locally, and push them to your own master branch.

Your (forked) repo should have an untouched `/answers` folder, and use the `/lessons` folder for all of your work when following along with the course.

### What if the repository gets updated after I've forked it?

If I update this repository, and you want to update your forked repository with my changes, then you'll want to [follow these steps to sync my changes to your repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/syncing-a-fork).

3 things that are really important here:
1. Do all of your work in a separate `/lessons` folder. If you make all of your changes in a brand new folder that isn't in this repository, then when you sync my changes to your forked repository it won't have any conflicts!
2. Linked the above, don't make changes to the `/answers` folder - or if you do, make sure you delete them afterwards. If I update the repository it's very likely I'll be updating this folder and it'll make things a lot harder for you!
3. **If you've made changes, and you sync your fork with my changes, don't discard your commits!** This will get rid of all of your progress. I'd advise creating a new branch before syncing in case this happens



