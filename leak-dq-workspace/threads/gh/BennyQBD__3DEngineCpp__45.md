# free(): invalid pointer: 

- URL: https://github.com/BennyQBD/3DEngineCpp/issues/45
- Repo: BennyQBD/3DEngineCpp (language: C)
- State: open; created 2018-08-17T06:35:00Z; status ok; passes main

## Issue body

reporter (NONE) · ynsbalci · 2018-08-17T06:35:00Z · https://github.com/BennyQBD/3DEngineCpp/issues/45

hi!
I've compiled the project in linux mint for codeblocks, but I get a pointer error. In "stb_image.c" the free() funcions is giving an error. what can i do?
thanks have a good day.


## Comment 510378109

other (NONE) · shivamprasad99 · 2019-07-11T08:06:35Z · https://github.com/BennyQBD/3DEngineCpp/issues/45#issuecomment-510378109

I am also getting same error:
free(): invalid pointer
Aborted (core dumped)
on building from the terminal in Ubuntu 18.04 
What should I do?

## Comment 1116327898

other (NONE) · Phobos03 · 2022-05-03T16:54:10Z · https://github.com/BennyQBD/3DEngineCpp/issues/45#issuecomment-1116327898

Hello, I know that this is old repo, but I also have the same issue like shivamprasad99 with free(): invalid pointer
Aborted (core dumped). Maybe someone resolve this issue already?  

## Comment 1200987724

other (NONE) · gedeschaines · 2022-08-01T10:03:08Z · https://github.com/BennyQBD/3DEngineCpp/issues/45#issuecomment-1200987724

**Fixes to prevent Policy warnings from syntax errors in CMake code files.**

1. File: ./cmake/FindGLEW.cmake
````
    insert: SET(PROGRAMFILESX86 "PROGRAMFILES(X86)")
    before: SET( GLEW_SEARCH_PATHS
    and
    change: "$ENV{PROGRAMFILES(X86)}/GLEW"   # WINDOWS
        to: "$ENV{${PROGRAMFILESX86}}/GLEW"     # WINDOWS
````

2. File: ./cmake/FindSDL2.cmake
````
    insert: SET(PROGRAMFILESX86 "PROGRAMFILES(X86)")
    before: SET( SDL2_SEARCH_PATHS
    and
    change: "$ENV{PROGRAMFILES(X86)}/SDL2"     # WINDOWS
        to: "$ENV{${PROGRAMFILESX86}}/SDL2"   # WINDOWS
````

3. File: ./cmake/FindASSIMP.cmake
````
    insert: SET(PROGRAMFILESX86 "PROGRAMFILES(X86)")
    before: SET( ASSIMP_SEARCH_PATHS
    and
    change: "$ENV{PROGRAMFILES(X86)}/ASSIMP"	# WINDOWS
        to: "$ENV{${PROGRAMFILESX86}}/ASSIMP"	# WINDOWS
````
     
**Fixes to prevent program execution abort on free(): invalid pointer.**

1. File: ./src/rendering/texture.h, line 60
````
    from: void operator=(Texture texture);
      to: Texture& operator=(Texture other) noexcept;
````

2. File: ./src/rendering/texture.cpp, lines 207-213

    replace:
````
    void Texture::operator=(Texture texture)
    {
        char* temp[sizeof(Texture)/sizeof(char)];
        memcpy(temp, this, sizeof(Texture));
	memcpy(this, &texture, sizeof(Texture));
        memcpy(&texture, temp, sizeof(Texture));
    }
````

      with:
````
    Texture& Texture::operator=(Texture other) noexcept
    {
        //Implemented using move assignment.
    
        //Guard self assignment
        if (this == &other)
            return *this;
    
        if(m_textureData && m_textureData->RemoveReference())
	{
            if(m_fileName.length() > 0)
                s_resourceMap.erase(m_fileName);
	    
	        delete m_textureData;
	}
	m_fileName = other.m_fileName;
        m_textureData = other.m_textureData;
        m_textureData->AddReference();
        return *this;
    }
````

