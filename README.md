# rpm-package-explorer
No more Ctrl+F to find RPM packages in repositories!

And good god ~~why did I commit to this~~ DNF repository data is complicated.

# "Oh no not another @chong601's project, now what?"
This is not fun.

![](.readme/goodlord.PNG)

Of course, I got interested and decided to make it a real thing.

![](.readme/whyudodis.PNG)

Not like I use RHEL on any of my systems. 

# Why not just copy DNF repository code and use that instead?
While DNF indeed uses Python, it depends on [Hawkey](https://github.com/rpm-software-management/libdnf/tree/dnf-4-master/python/hawkey) which provides repository data parsing which is written in C.

It is not possible to bring this with the app as it requires compiling from source to generate the Python modules. 

It's easier (for now) to just reimplement those that I need to use by clean-room-ish reverse-engineering.

# License
rpm-package-explorer is released under the MIT License. Refer to LICENSE file for the full license text.