- Not sure about Docker image size, as I have little experience with this. 
- GPG secret creation may contain issues as I was not able to create "real" GPG key which I could use in testing.
- Security issues:
  - Regarding SSH secret creation: I would prefer storing `contents` encoded (or preferably hashed) rather than in plain text.
- Structure of project
  - I tried to maintain most of the previous structure (as it is "active project", and probably used by other projects as well)
    - However, skeleton of project was created with one type of secret in mind.
    - So the result is created in a way that most of API I/O stays the same and primarily core of project is changed.