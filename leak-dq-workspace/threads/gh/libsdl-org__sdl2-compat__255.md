# sdl2-compat not compatable with SDL2 code. Causes false positives on memory leaks.

- URL: https://github.com/libsdl-org/sdl2-compat/issues/255
- Repo: libsdl-org/sdl2-compat (language: C)
- State: open; created 2025-01-29T10:43:04Z; status ok; passes main

## Issue body

reporter (NONE) · ProgrammingRainbow · 2025-01-29T10:43:04Z · https://github.com/libsdl-org/sdl2-compat/issues/255

System is Archlinux, KDE, X11, AMD ai 9 hx 370 using the 6.13 testing kernel.

Archlinux recently replaced there SDL2 package with SDL2-compat and added SDL3. This seems to have broken all of my SDL2 projects. I compile strict debugging and sanitizer to help to diminish the chance of coding mistakes. Again this seems to have broken all of my projects. So this sdl2-compat is not currently compatible with sdl2 at least not fully. But it seems archlinux no longer has the real sdl2 package.

src/main.h
```c
#ifndef MAIN_H
#define MAIN_H

#include <SDL2/SDL.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define SDL_FLAGS (SDL_INIT_VIDEO | SDL_INIT_AUDIO)

#define WINDOW_TITLE "Tetris"
#define WINDOW_WIDTH 720
#define WINDOW_HEIGHT 600

#endif
```
src/main.c
```c
#include "game.h"

int main(void) {
    bool exit_status = EXIT_FAILURE;

    struct Game *game = NULL;

    if (game_new(&game)) {
        game_run(game);
        exit_status = EXIT_SUCCESS;
    }

    game_free(&game);

    return exit_status;
}
```
src/init_sdl.h
```c
#ifndef INIT_SDL_H
#define INIT_SDL_H

#include "game.h"

bool game_init_sdl(struct Game *g);

#endif
```
src/init_sdl.c
```c
#include "init_sdl.h"

bool game_init_sdl(struct Game *g) {
    if (SDL_Init(SDL_FLAGS)) {
        fprintf(stderr, "Error initializing SDL: %s\n", SDL_GetError());
        return false;
    }

    g->window = SDL_CreateWindow(WINDOW_TITLE, SDL_WINDOWPOS_CENTERED,
                                 SDL_WINDOWPOS_CENTERED, WINDOW_WIDTH,
                                 WINDOW_HEIGHT, 0);
    if (!g->window) {
        fprintf(stderr, "Error creating window: %s\n", SDL_GetError());
        return false;
    }

    g->renderer = SDL_CreateRenderer(g->window, -1, SDL_RENDERER_ACCELERATED);
    if (!g->renderer) {
        fprintf(stderr, "Error creating renderer: %s\n", SDL_GetError());
        return false;
    }

    return true;
}
```
src/game.h
```c
#ifndef GAME_H
#define GAME_H

#include "main.h"

struct Game {
        SDL_Event event;
        SDL_Window *window;
        SDL_Renderer *renderer;
        bool is_running;
};

bool game_new(struct Game **game);
void game_free(struct Game **game);
void game_run(struct Game *g);

#endif
```
src/game.c
```c
#include "game.h"
#include "init_sdl.h"

void game_events(struct Game *g);
void game_update(struct Game *g);
void game_draw(const struct Game *g);

bool game_new(struct Game **game) {
    *game = calloc(1, sizeof(struct Game));
    if (*game == NULL) {
        fprintf(stderr, "Error in calloc of new game.\n");
        return false;
    }
    struct Game *g = *game;

    g->is_running = true;

    if (!game_init_sdl(g)) {
        return false;
    }

    return true;
}

void game_free(struct Game **game) {
    if (*game) {
        struct Game *g = *game;

        if (g->renderer) {
            SDL_DestroyRenderer(g->renderer);
            g->renderer = NULL;
        }

        if (g->window) {
            SDL_DestroyWindow(g->window);
            g->window = NULL;
        }

        SDL_Quit();

        g = NULL;

        free(*game);
        *game = NULL;

        printf("all clean!\n");
    }
}

void game_events(struct Game *g) {
    while (SDL_PollEvent(&g->event)) {
        switch (g->event.type) {
        case SDL_QUIT:
            g->is_running = false;
            break;
        case SDL_KEYDOWN:
            switch (g->event.key.keysym.scancode) {
            case SDL_SCANCODE_ESCAPE:
                g->is_running = false;
                break;
            default:
                break;
            }
            break;
        default:
            break;
        }
    }
}

void game_draw(const struct Game *g) {
    SDL_RenderClear(g->renderer);

    SDL_RenderPresent(g->renderer);
}

void game_run(struct Game *g) {
    while (g->is_running) {

        game_events(g);

        game_draw(g);

        SDL_Delay(16);
    }
}
```
Makefile
```make
TARGET			= tetris
BUILD_DIR		= .build
SRC_DIR			?= src
CC				?= gcc

CFLAGS_BASE     = -std=c11 -Wstrict-aliasing=2 -Wall -Wextra -Werror \
                  -Wpedantic -Wwrite-strings -Wconversion -Wmissing-declarations \
                  -Wmissing-include-dirs -Wfloat-equal -Wsign-compare -Wundef \
                  -Wcast-align -Wswitch-default -Wimplicit-fallthrough \
                  -Wempty-body -Wuninitialized -Wmisleading-indentation \
                  -Wshadow -Wmissing-prototypes -Wstrict-prototypes -Wold-style-definition

CFLAGS_RELEASE	= -O3 -march=native -flto=auto -fno-plt -fomit-frame-pointer

CFLAGS_DEBUG 	= -O0 -g3 -ggdb3 -fno-strict-aliasing -fstack-protector-strong \
				  -DDEBUG -fno-omit-frame-pointer

LDLIBS_BASE		=

LDLIBS_RELEASE	= -flto

LDLIBS_DEBUG	=

SRCS			= $(wildcard $(SRC_DIR)/*.c)
OBJS			= $(addprefix $(BUILD_DIR)/, $(notdir $(SRCS:.c=.o)))
DEPS			= $(OBJS:.o=.d)

ifeq ($(OS),Windows_NT)
	PKG_CONFIG := $(shell where pkg-config >NUL 2>&1 && echo "yes" || echo "no")
	CLEAN 		= del /f $(TARGET).exe & if exist $(BUILD_DIR) rmdir /s /q $(BUILD_DIR)
	MKDIR		= if not exist $(BUILD_DIR) mkdir
else
	CFLAGS_DEBUG	+= -fsanitize=address -fsanitize-address-use-after-scope \
					   -ftrapv
	LDLIBS_DEBUG	+= -fsanitize=address -fsanitize-address-use-after-scope
	PKG_CONFIG := $(shell command -v pkg-config >/dev/null 2>&1 && echo "yes" || echo "no")
	CLEAN		= $(RM) -f $(TARGET) && $(RM) -rf $(BUILD_DIR)
	MKDIR		= mkdir -p $(BUILD_DIR)
endif

ifeq ($(PKG_CONFIG),yes)
    CFLAGS_BASE += $(shell pkg-config --cflags sdl2 SDL2_image SDL2_ttf)
    LDLIBS_BASE += $(shell pkg-config --libs sdl2 SDL2_image SDL2_ttf)
else
    $(error "pkg-config is not available. Please install pkg-config.")
endif

CFLAGS		?= $(CFLAGS_BASE) $(CFLAGS_DEBUG)
LDLIBS		?= $(LDLIBS_BASE) $(LDLIBS_DEBUG)

$(BUILD_DIR):
	$(MKDIR)

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@

$(TARGET): $(OBJS)
	$(CC) $^ -o $@ $(LDLIBS)

-include $(DEPS)

.PHONY: all clean run rebuild release

all: $(TARGET)

release: CFLAGS = $(CFLAGS_BASE) $(CFLAGS_RELEASE)
release: LDLIBS = $(LDLIBS_BASE) $(LDLIBS_RELEASE)
release: all

clean:
	$(CLEAN)

run: $(TARGET)
	./$<

rebuild: clean all
```

```
=================================================================
==3842==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 520 byte(s) in 13 object(s) allocated from:
    #0 0x701099cfd891 in malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x701098b525ea  (<unknown module>)
    #2 0x701098b47094  (/home/jeremiah/Tetris/C-SDL2/tetris+0x14094)
    #3 0x70108c386766  (/usr/lib/../lib/libSDL3.so.0+0x186766) (BuildId: 3c9f784f4962261f7624483ae4bd4
029a31f8e32)
    #4 0x70108c21c511  (/usr/lib/../lib/libSDL3.so.0+0x1c511) (BuildId: 3c9f784f4962261f7624483ae4bd40
29a31f8e32)
    #5 0x70109a403293  (/usr/lib/libSDL2-2.0.so.0+0x1a293) (BuildId: 70b531bd0eff55bb9a6cffca84c136d70
2321a2c)
    #6 0x605fa9634818 in game_init_sdl Video01/init_sdl.c:4
    #7 0x605fa96343ee in game_new Video01/game.c:18
    #8 0x605fa9634b00 in main Video01/main.c:8
    #9 0x701099a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a
)
    #10 0x701099a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc1229
6052529af22f6a450a75a)
    #11 0x605fa9634204 in _start (/home/jeremiah/Tetris/C-SDL2/tetris+0x2204) (BuildId: b39dd191a269b3
185f6705dab0f2a65492e45aa9)

Direct leak of 368 byte(s) in 2 object(s) allocated from:
    #0 0x701099cfd1aa in calloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x701098b40ac3  (/home/jeremiah/Tetris/C-SDL2/tetris+0xdac3)
    #2 0x701098b42bbd  (/home/jeremiah/Tetris/C-SDL2/tetris+0xfbbd)
    #3 0x701098b4d8ce  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1a8ce)
    #4 0x701098b4dac7  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1aac7)
    #5 0x701098b4de20  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1ae20)
    #6 0x701098b4e3ac  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1b3ac)
    #7 0x701098b31e82  (<unknown module>)
    #8 0x701098b46b9f  (/home/jeremiah/Tetris/C-SDL2/tetris+0x13b9f)
    #9 0x701098b33d36  (<unknown module>)
    #10 0x701098b33fdd  (<unknown module>)
    #11 0x701098b342ca  (<unknown module>)
    #12 0x70108c3867b7  (/usr/lib/../lib/libSDL3.so.0+0x1867b7) (BuildId: 3c9f784f4962261f7624483ae4bd
4029a31f8e32)
    #13 0x70108c21c511  (/usr/lib/../lib/libSDL3.so.0+0x1c511) (BuildId: 3c9f784f4962261f7624483ae4bd4
029a31f8e32)
    #14 0x70109a403293  (/usr/lib/libSDL2-2.0.so.0+0x1a293) (BuildId: 70b531bd0eff55bb9a6cffca84c136d7
02321a2c)
    #15 0x605fa9634818 in game_init_sdl Video01/init_sdl.c:4
    #16 0x605fa96343ee in game_new Video01/game.c:18
    #17 0x605fa9634b00 in main Video01/main.c:8
    #18 0x701099a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75
a)
    #19 0x701099a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc1229
6052529af22f6a450a75a)
    #20 0x605fa9634204 in _start (/home/jeremiah/Tetris/C-SDL2/tetris+0x2204) (BuildId: b39dd191a269b3
185f6705dab0f2a65492e45aa9)

Direct leak of 368 byte(s) in 2 object(s) allocated from:
    #0 0x701099cfd1aa in calloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x701098b40ac3  (/home/jeremiah/Tetris/C-SDL2/tetris+0xdac3)
    #2 0x701098b42bbd  (/home/jeremiah/Tetris/C-SDL2/tetris+0xfbbd)
    #3 0x701098b4d8ce  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1a8ce)
    #4 0x701098b4dac7  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1aac7)
    #5 0x701098b4de20  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1ae20)
    #6 0x701098b4e3ac  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1b3ac)
    #7 0x701098b31e82  (<unknown module>)
    #8 0x701098b46b9f  (/home/jeremiah/Tetris/C-SDL2/tetris+0x13b9f)
    #9 0x701098b33d36  (<unknown module>)
    #10 0x701098b33fdd  (<unknown module>)
    #11 0x701098b342ca  (<unknown module>)
    #12 0x70108c386786  (/usr/lib/../lib/libSDL3.so.0+0x186786) (BuildId: 3c9f784f4962261f7624483ae4bd
4029a31f8e32)
    #13 0x70108c21c511  (/usr/lib/../lib/libSDL3.so.0+0x1c511) (BuildId: 3c9f784f4962261f7624483ae4bd4
029a31f8e32)
    #14 0x70109a403293  (/usr/lib/libSDL2-2.0.so.0+0x1a293) (BuildId: 70b531bd0eff55bb9a6cffca84c136d7
02321a2c)
    #15 0x605fa9634818 in game_init_sdl Video01/init_sdl.c:4
    #16 0x605fa96343ee in game_new Video01/game.c:18
    #17 0x605fa9634b00 in main Video01/main.c:8
    #18 0x701099a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75
a)
    #19 0x701099a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc1229
6052529af22f6a450a75a)
    #20 0x605fa9634204 in _start (/home/jeremiah/Tetris/C-SDL2/tetris+0x2204) (BuildId: b39dd191a269b3
185f6705dab0f2a65492e45aa9)

Direct leak of 184 byte(s) in 1 object(s) allocated from:
    #0 0x701099cfd1aa in calloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x701098b40ac3  (/home/jeremiah/Tetris/C-SDL2/tetris+0xdac3)
    #2 0x701098b41948  (/home/jeremiah/Tetris/C-SDL2/tetris+0xe948)
    #3 0x701098b33fbd  (<unknown module>)
    #4 0x701098b342ca  (<unknown module>)
    #5 0x70108c386786  (/usr/lib/../lib/libSDL3.so.0+0x186786) (BuildId: 3c9f784f4962261f7624483ae4bd4
029a31f8e32)
    #6 0x70108c21c511  (/usr/lib/../lib/libSDL3.so.0+0x1c511) (BuildId: 3c9f784f4962261f7624483ae4bd40
29a31f8e32)
    #7 0x70109a403293  (/usr/lib/libSDL2-2.0.so.0+0x1a293) (BuildId: 70b531bd0eff55bb9a6cffca84c136d70
2321a2c)
    #8 0x605fa9634818 in game_init_sdl Video01/init_sdl.c:4
    #9 0x605fa96343ee in game_new Video01/game.c:18
    #10 0x605fa9634b00 in main Video01/main.c:8
    #11 0x701099a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75
a)
    #12 0x701099a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc1229
6052529af22f6a450a75a)
    #13 0x605fa9634204 in _start (/home/jeremiah/Tetris/C-SDL2/tetris+0x2204) (BuildId: b39dd191a269b3
185f6705dab0f2a65492e45aa9)

Direct leak of 38 byte(s) in 1 object(s) allocated from:
    #0 0x701099cfd891 in malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x701098b4f345  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1c345)
    #2 0x701098b344b2  (<unknown module>)
    #3 0x70108c386786  (/usr/lib/../lib/libSDL3.so.0+0x186786) (BuildId: 3c9f784f4962261f7624483ae4bd4
029a31f8e32)
    #4 0x70108c21c511  (/usr/lib/../lib/libSDL3.so.0+0x1c511) (BuildId: 3c9f784f4962261f7624483ae4bd40
29a31f8e32)
    #5 0x70109a403293  (/usr/lib/libSDL2-2.0.so.0+0x1a293) (BuildId: 70b531bd0eff55bb9a6cffca84c136d70
2321a2c)
    #6 0x605fa9634818 in game_init_sdl Video01/init_sdl.c:4
    #7 0x605fa96343ee in game_new Video01/game.c:18
    #8 0x605fa9634b00 in main Video01/main.c:8
    #9 0x701099a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a
)
    #10 0x701099a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc1229
6052529af22f6a450a75a)
    #11 0x605fa9634204 in _start (/home/jeremiah/Tetris/C-SDL2/tetris+0x2204) (BuildId: b39dd191a269b3
185f6705dab0f2a65492e45aa9)

Direct leak of 29 byte(s) in 1 object(s) allocated from:
    #0 0x701099cfd891 in malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x701098b4f345  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1c345)
    #2 0x701098b3467b  (<unknown module>)
    #3 0x70108c386786  (/usr/lib/../lib/libSDL3.so.0+0x186786) (BuildId: 3c9f784f4962261f7624483ae4bd4
029a31f8e32)
    #4 0x70108c21c511  (/usr/lib/../lib/libSDL3.so.0+0x1c511) (BuildId: 3c9f784f4962261f7624483ae4bd40
29a31f8e32)
    #5 0x70109a403293  (/usr/lib/libSDL2-2.0.so.0+0x1a293) (BuildId: 70b531bd0eff55bb9a6cffca84c136d70
2321a2c)
    #6 0x605fa9634818 in game_init_sdl Video01/init_sdl.c:4
    #7 0x605fa96343ee in game_new Video01/game.c:18
    #8 0x605fa9634b00 in main Video01/main.c:8
    #9 0x701099a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a
)
    #10 0x701099a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc1229
6052529af22f6a450a75a)
    #11 0x605fa9634204 in _start (/home/jeremiah/Tetris/C-SDL2/tetris+0x2204) (BuildId: b39dd191a269b3
185f6705dab0f2a65492e45aa9)

Direct leak of 29 byte(s) in 1 object(s) allocated from:
    #0 0x701099cfd891 in malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x701098b4f345  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1c345)
    #2 0x701098b346c8  (<unknown module>)
    #3 0x70108c386786  (/usr/lib/../lib/libSDL3.so.0+0x186786) (BuildId: 3c9f784f4962261f7624483ae4bd4
029a31f8e32)
    #4 0x70108c21c511  (/usr/lib/../lib/libSDL3.so.0+0x1c511) (BuildId: 3c9f784f4962261f7624483ae4bd40
29a31f8e32)
    #5 0x70109a403293  (/usr/lib/libSDL2-2.0.so.0+0x1a293) (BuildId: 70b531bd0eff55bb9a6cffca84c136d70
2321a2c)
    #6 0x605fa9634818 in game_init_sdl Video01/init_sdl.c:4
    #7 0x605fa96343ee in game_new Video01/game.c:18
    #8 0x605fa9634b00 in main Video01/main.c:8
    #9 0x701099a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a
)
    #10 0x701099a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc1229
6052529af22f6a450a75a)
    #11 0x605fa9634204 in _start (/home/jeremiah/Tetris/C-SDL2/tetris+0x2204) (BuildId: b39dd191a269b3
185f6705dab0f2a65492e45aa9)

Direct leak of 24 byte(s) in 1 object(s) allocated from:
    #0 0x701099cfd891 in malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x701098b57498  (<unknown module>)
    #2 0x701098b41796  (/home/jeremiah/Tetris/C-SDL2/tetris+0xe796)
    #3 0x701098b45b31  (/home/jeremiah/Tetris/C-SDL2/tetris+0x12b31)
    #4 0x701098b33d4d  (<unknown module>)
    #5 0x701098b33fdd  (<unknown module>)
    #6 0x701098b342ca  (<unknown module>)
    #7 0x70108c386786  (/usr/lib/../lib/libSDL3.so.0+0x186786) (BuildId: 3c9f784f4962261f7624483ae4bd4
029a31f8e32)
    #8 0x70108c21c511  (/usr/lib/../lib/libSDL3.so.0+0x1c511) (BuildId: 3c9f784f4962261f7624483ae4bd40
29a31f8e32)
    #9 0x70109a403293  (/usr/lib/libSDL2-2.0.so.0+0x1a293) (BuildId: 70b531bd0eff55bb9a6cffca84c136d70
2321a2c)
    #10 0x605fa9634818 in game_init_sdl Video01/init_sdl.c:4
    #11 0x605fa96343ee in game_new Video01/game.c:18
    #12 0x605fa9634b00 in main Video01/main.c:8
    #13 0x701099a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75
a)
    #14 0x701099a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc1229
6052529af22f6a450a75a)
    #15 0x605fa9634204 in _start (/home/jeremiah/Tetris/C-SDL2/tetris+0x2204) (BuildId: b39dd191a269b3
185f6705dab0f2a65492e45aa9)

Direct leak of 8 byte(s) in 1 object(s) allocated from:
    #0 0x701099cfd891 in malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x70108c31c54e  (/usr/lib/../lib/libSDL3.so.0+0x11c54e) (BuildId: 3c9f784f4962261f7624483ae4bd4
029a31f8e32)
    #2 0x70109a404a1b  (/usr/lib/libSDL2-2.0.so.0+0x1ba1b) (BuildId: 70b531bd0eff55bb9a6cffca84c136d70
2321a2c)
    #3 0x70109a4056d7  (/usr/lib/libSDL2-2.0.so.0+0x1c6d7) (BuildId: 70b531bd0eff55bb9a6cffca84c136d70
2321a2c)
    #4 0x70109a40576c  (/usr/lib/libSDL2-2.0.so.0+0x1c76c) (BuildId: 70b531bd0eff55bb9a6cffca84c136d70
2321a2c)
    #5 0x605fa963489d in game_init_sdl Video01/init_sdl.c:9
    #6 0x605fa96343ee in game_new Video01/game.c:18
    #7 0x605fa9634b00 in main Video01/main.c:8
    #8 0x701099a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a
)
    #9 0x701099a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc12296
052529af22f6a450a75a)
    #10 0x605fa9634204 in _start (/home/jeremiah/Tetris/C-SDL2/tetris+0x2204) (BuildId: b39dd191a269b3
185f6705dab0f2a65492e45aa9)

Direct leak of 8 byte(s) in 1 object(s) allocated from:
    #0 0x701099cfd891 in malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x70108c31c54e  (/usr/lib/../lib/libSDL3.so.0+0x11c54e) (BuildId: 3c9f784f4962261f7624483ae4bd4
029a31f8e32)
    #2 0x70109a404a1b  (/usr/lib/libSDL2-2.0.so.0+0x1ba1b) (BuildId: 70b531bd0eff55bb9a6cffca84c136d70
2321a2c)
    #3 0x70109a4056e7  (/usr/lib/libSDL2-2.0.so.0+0x1c6e7) (BuildId: 70b531bd0eff55bb9a6cffca84c136d70
2321a2c)
    #4 0x70109a40576c  (/usr/lib/libSDL2-2.0.so.0+0x1c76c) (BuildId: 70b531bd0eff55bb9a6cffca84c136d70
2321a2c)
    #5 0x605fa963489d in game_init_sdl Video01/init_sdl.c:9
    #6 0x605fa96343ee in game_new Video01/game.c:18
    #7 0x605fa9634b00 in main Video01/main.c:8
    #8 0x701099a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a
)
    #9 0x701099a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc12296
052529af22f6a450a75a)
    #10 0x605fa9634204 in _start (/home/jeremiah/Tetris/C-SDL2/tetris+0x2204) (BuildId: b39dd191a269b3
185f6705dab0f2a65492e45aa9)

Indirect leak of 352 byte(s) in 1 object(s) allocated from:
    #0 0x701099cfc542 in realloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:85
    #1 0x701098b5086d  (<unknown module>)
    #2 0x701098b54c2f  (<unknown module>)
    #3 0x701098b3c8bf  (/home/jeremiah/Tetris/C-SDL2/tetris+0x98bf)
    #4 0x701098b3cbf8  (/home/jeremiah/Tetris/C-SDL2/tetris+0x9bf8)
    #5 0x701098b3d1b6  (/home/jeremiah/Tetris/C-SDL2/tetris+0xa1b6)
    #6 0x701098b3d334  (/home/jeremiah/Tetris/C-SDL2/tetris+0xa334)
    #7 0x701098b412ed  (/home/jeremiah/Tetris/C-SDL2/tetris+0xe2ed)
    #8 0x701098b42768  (/home/jeremiah/Tetris/C-SDL2/tetris+0xf768)
    #9 0x70108c37e965  (/usr/lib/../lib/libSDL3.so.0+0x17e965) (BuildId: 3c9f784f4962261f7624483ae4bd4
029a31f8e32)
    #10 0x70108c38563e  (/usr/lib/../lib/libSDL3.so.0+0x18563e) (BuildId: 3c9f784f4962261f7624483ae4bd
4029a31f8e32)
    #11 0x70108c3858e9  (/usr/lib/../lib/libSDL3.so.0+0x1858e9) (BuildId: 3c9f784f4962261f7624483ae4bd
4029a31f8e32)
    #12 0x70108c34c2b1  (/usr/lib/../lib/libSDL3.so.0+0x14c2b1) (BuildId: 3c9f784f4962261f7624483ae4bd
4029a31f8e32)
    #13 0x70108c32c115  (/usr/lib/../lib/libSDL3.so.0+0x12c115) (BuildId: 3c9f784f4962261f7624483ae4bd
4029a31f8e32)
    #14 0x70108c21b4b7  (/usr/lib/../lib/libSDL3.so.0+0x1b4b7) (BuildId: 3c9f784f4962261f7624483ae4bd4
029a31f8e32)
    #15 0x70108c21b6a4  (/usr/lib/../lib/libSDL3.so.0+0x1b6a4) (BuildId: 3c9f784f4962261f7624483ae4bd4
029a31f8e32)
    #16 0x70109a40347b  (/usr/lib/libSDL2-2.0.so.0+0x1a47b) (BuildId: 70b531bd0eff55bb9a6cffca84c136d7
02321a2c)
    #17 0x605fa9634536 in game_free Video01/game.c:39
    #18 0x605fa9634b47 in main Video01/main.c:13
    #19 0x701099a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75
a)
    #20 0x701099a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc1229
6052529af22f6a450a75a)
    #21 0x605fa9634204 in _start (/home/jeremiah/Tetris/C-SDL2/tetris+0x2204) (BuildId: b39dd191a269b3
185f6705dab0f2a65492e45aa9)

Indirect leak of 320 byte(s) in 1 object(s) allocated from:
    #0 0x701099cfc542 in realloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:85
    #1 0x701098b5086d  (<unknown module>)
    #2 0x701098b3c3e4  (/home/jeremiah/Tetris/C-SDL2/tetris+0x93e4)
    #3 0x701098b3c8bf  (/home/jeremiah/Tetris/C-SDL2/tetris+0x98bf)
    #4 0x701098b3ccad  (/home/jeremiah/Tetris/C-SDL2/tetris+0x9cad)
    #5 0x701098b3d1b6  (/home/jeremiah/Tetris/C-SDL2/tetris+0xa1b6)
    #6 0x701098b3d334  (/home/jeremiah/Tetris/C-SDL2/tetris+0xa334)
    #7 0x701098b412ed  (/home/jeremiah/Tetris/C-SDL2/tetris+0xe2ed)
    #8 0x701098b42768  (/home/jeremiah/Tetris/C-SDL2/tetris+0xf768)
    #9 0x701098b429df  (/home/jeremiah/Tetris/C-SDL2/tetris+0xf9df)
    #10 0x701098b354af  (<unknown module>)
    #11 0x70108c386f4d  (/usr/lib/../lib/libSDL3.so.0+0x186f4d) (BuildId: 3c9f784f4962261f7624483ae4bd
4029a31f8e32)
    #12 0x70108c35aa61  (/usr/lib/../lib/libSDL3.so.0+0x15aa61) (BuildId: 3c9f784f4962261f7624483ae4bd
4029a31f8e32)
    #13 0x70108c21d63e  (/usr/lib/../lib/libSDL3.so.0+0x1d63e) (BuildId: 3c9f784f4962261f7624483ae4bd4
029a31f8e32)
    #14 0x70109a403293  (/usr/lib/libSDL2-2.0.so.0+0x1a293) (BuildId: 70b531bd0eff55bb9a6cffca84c136d7
02321a2c)
    #15 0x605fa9634818 in game_init_sdl Video01/init_sdl.c:4
    #16 0x605fa96343ee in game_new Video01/game.c:18
    #17 0x605fa9634b00 in main Video01/main.c:8
    #18 0x701099a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75
a)
    #19 0x701099a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc1229
6052529af22f6a450a75a)
    #20 0x605fa9634204 in _start (/home/jeremiah/Tetris/C-SDL2/tetris+0x2204) (BuildId: b39dd191a269b3
185f6705dab0f2a65492e45aa9)

Indirect leak of 223 byte(s) in 1 object(s) allocated from:
    #0 0x701099cfc542 in realloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:85
    #1 0x701098b4f5a6  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1c5a6)
    #2 0x701098b4f634  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1c634)
    #3 0x701098b5121b  (<unknown module>)
    #4 0x701098b53bdc  (<unknown module>)
    #5 0x701098b3cab4  (/home/jeremiah/Tetris/C-SDL2/tetris+0x9ab4)
    #6 0x701098b412e2  (/home/jeremiah/Tetris/C-SDL2/tetris+0xe2e2)
    #7 0x701098b41edc  (/home/jeremiah/Tetris/C-SDL2/tetris+0xeedc)
    #8 0x701098b33930  (<unknown module>)
    #9 0x701098b33d1b  (<unknown module>)
    #10 0x70108c386fb6  (/usr/lib/../lib/libSDL3.so.0+0x186fb6) (BuildId: 3c9f784f4962261f7624483ae4bd
4029a31f8e32)
    #11 0x70108c35aa61  (/usr/lib/../lib/libSDL3.so.0+0x15aa61) (BuildId: 3c9f784f4962261f7624483ae4bd
4029a31f8e32)
    #12 0x70108c21d63e  (/usr/lib/../lib/libSDL3.so.0+0x1d63e) (BuildId: 3c9f784f4962261f7624483ae4bd4
029a31f8e32)
    #13 0x70109a403293  (/usr/lib/libSDL2-2.0.so.0+0x1a293) (BuildId: 70b531bd0eff55bb9a6cffca84c136d7
02321a2c)
    #14 0x605fa9634818 in game_init_sdl Video01/init_sdl.c:4
    #15 0x605fa96343ee in game_new Video01/game.c:18
    #16 0x605fa9634b00 in main Video01/main.c:8
    #17 0x701099a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75
a)
    #18 0x701099a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc1229
6052529af22f6a450a75a)
    #19 0x605fa9634204 in _start (/home/jeremiah/Tetris/C-SDL2/tetris+0x2204) (BuildId: b39dd191a269b3
185f6705dab0f2a65492e45aa9)

Indirect leak of 223 byte(s) in 1 object(s) allocated from:
    #0 0x701099cfc542 in realloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:85
    #1 0x701098b4f5a6  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1c5a6)
    #2 0x701098b4f634  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1c634)
    #3 0x701098b5121b  (<unknown module>)
    #4 0x701098b53bdc  (<unknown module>)
    #5 0x701098b3cab4  (/home/jeremiah/Tetris/C-SDL2/tetris+0x9ab4)
    #6 0x701098b412e2  (/home/jeremiah/Tetris/C-SDL2/tetris+0xe2e2)
    #7 0x701098b41edc  (/home/jeremiah/Tetris/C-SDL2/tetris+0xeedc)
    #8 0x701098b33930  (<unknown module>)
    #9 0x701098b33d1b  (<unknown module>)
    #10 0x701098b33fdd  (<unknown module>)
    #11 0x701098b342ca  (<unknown module>)
    #12 0x70108c3867b7  (/usr/lib/../lib/libSDL3.so.0+0x1867b7) (BuildId: 3c9f784f4962261f7624483ae4bd
4029a31f8e32)
    #13 0x70108c21c511  (/usr/lib/../lib/libSDL3.so.0+0x1c511) (BuildId: 3c9f784f4962261f7624483ae4bd4
029a31f8e32)
    #14 0x70109a403293  (/usr/lib/libSDL2-2.0.so.0+0x1a293) (BuildId: 70b531bd0eff55bb9a6cffca84c136d7
02321a2c)
    #15 0x605fa9634818 in game_init_sdl Video01/init_sdl.c:4
    #16 0x605fa96343ee in game_new Video01/game.c:18
    #17 0x605fa9634b00 in main Video01/main.c:8
    #18 0x701099a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75
a)
    #19 0x701099a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc1229
6052529af22f6a450a75a)
    #20 0x605fa9634204 in _start (/home/jeremiah/Tetris/C-SDL2/tetris+0x2204) (BuildId: b39dd191a269b3
185f6705dab0f2a65492e45aa9)

Indirect leak of 223 byte(s) in 1 object(s) allocated from:
    #0 0x701099cfc542 in realloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:85
    #1 0x701098b4f5a6  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1c5a6)
    #2 0x701098b4f634  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1c634)
    #3 0x701098b5121b  (<unknown module>)
    #4 0x701098b53bdc  (<unknown module>)
    #5 0x701098b3cab4  (/home/jeremiah/Tetris/C-SDL2/tetris+0x9ab4)
    #6 0x701098b412e2  (/home/jeremiah/Tetris/C-SDL2/tetris+0xe2e2)
    #7 0x701098b41edc  (/home/jeremiah/Tetris/C-SDL2/tetris+0xeedc)
    #8 0x701098b33930  (<unknown module>)
    #9 0x701098b33d1b  (<unknown module>)
    #10 0x70108c382fcf  (/usr/lib/../lib/libSDL3.so.0+0x182fcf) (BuildId: 3c9f784f4962261f7624483ae4bd
4029a31f8e32)
    #11 0x70108c3854de  (/usr/lib/../lib/libSDL3.so.0+0x1854de) (BuildId: 3c9f784f4962261f7624483ae4bd
4029a31f8e32)
    #12 0x70108c385b5d  (/usr/lib/../lib/libSDL3.so.0+0x185b5d) (BuildId: 3c9f784f4962261f7624483ae4bd
4029a31f8e32)
    #13 0x70108c34c2b1  (/usr/lib/../lib/libSDL3.so.0+0x14c2b1) (BuildId: 3c9f784f4962261f7624483ae4bd
4029a31f8e32)
    #14 0x70108c21ddaf  (/usr/lib/../lib/libSDL3.so.0+0x1ddaf) (BuildId: 3c9f784f4962261f7624483ae4bd4
029a31f8e32)
    #15 0x70109a403293  (/usr/lib/libSDL2-2.0.so.0+0x1a293) (BuildId: 70b531bd0eff55bb9a6cffca84c136d7
02321a2c)
    #16 0x605fa9634818 in game_init_sdl Video01/init_sdl.c:4
    #17 0x605fa96343ee in game_new Video01/game.c:18
    #18 0x605fa9634b00 in main Video01/main.c:8
    #19 0x701099a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75
a)
    #20 0x701099a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc1229
6052529af22f6a450a75a)
    #21 0x605fa9634204 in _start (/home/jeremiah/Tetris/C-SDL2/tetris+0x2204) (BuildId: b39dd191a269b3
185f6705dab0f2a65492e45aa9)

Indirect leak of 168 byte(s) in 1 object(s) allocated from:
    #0 0x701099cfc542 in realloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:85
    #1 0x701098b4f5a6  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1c5a6)
    #2 0x701098b4f634  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1c634)
    #3 0x701098b5121b  (<unknown module>)
    #4 0x701098b42bfd  (/home/jeremiah/Tetris/C-SDL2/tetris+0xfbfd)
    #5 0x701098b4d8ce  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1a8ce)
    #6 0x701098b4dac7  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1aac7)
    #7 0x701098b4de20  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1ae20)
    #8 0x701098b4e3ac  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1b3ac)
    #9 0x701098b31e82  (<unknown module>)
    #10 0x701098b46b9f  (/home/jeremiah/Tetris/C-SDL2/tetris+0x13b9f)
    #11 0x701098b33d36  (<unknown module>)
    #12 0x701098b33fdd  (<unknown module>)
    #13 0x701098b342ca  (<unknown module>)
    #14 0x70108c3867b7  (/usr/lib/../lib/libSDL3.so.0+0x1867b7) (BuildId: 3c9f784f4962261f7624483ae4bd
4029a31f8e32)
    #15 0x70108c21c511  (/usr/lib/../lib/libSDL3.so.0+0x1c511) (BuildId: 3c9f784f4962261f7624483ae4bd4
029a31f8e32)
    #16 0x70109a403293  (/usr/lib/libSDL2-2.0.so.0+0x1a293) (BuildId: 70b531bd0eff55bb9a6cffca84c136d7
02321a2c)
    #17 0x605fa9634818 in game_init_sdl Video01/init_sdl.c:4
    #18 0x605fa96343ee in game_new Video01/game.c:18
    #19 0x605fa9634b00 in main Video01/main.c:8
    #20 0x701099a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75
a)
    #21 0x701099a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc1229
6052529af22f6a450a75a)
    #22 0x605fa9634204 in _start (/home/jeremiah/Tetris/C-SDL2/tetris+0x2204) (BuildId: b39dd191a269b3
185f6705dab0f2a65492e45aa9)

Indirect leak of 168 byte(s) in 1 object(s) allocated from:
    #0 0x701099cfc542 in realloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:85
    #1 0x701098b4f5a6  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1c5a6)
    #2 0x701098b4f634  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1c634)
    #3 0x701098b5121b  (<unknown module>)
    #4 0x701098b42bfd  (/home/jeremiah/Tetris/C-SDL2/tetris+0xfbfd)
    #5 0x701098b4d8ce  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1a8ce)
    #6 0x701098b4dac7  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1aac7)
    #7 0x701098b4de20  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1ae20)
    #8 0x701098b4e3ac  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1b3ac)
    #9 0x701098b31e82  (<unknown module>)
    #10 0x701098b46b9f  (/home/jeremiah/Tetris/C-SDL2/tetris+0x13b9f)
    #11 0x701098b33d36  (<unknown module>)
    #12 0x701098b33fdd  (<unknown module>)
    #13 0x701098b342ca  (<unknown module>)
    #14 0x70108c386786  (/usr/lib/../lib/libSDL3.so.0+0x186786) (BuildId: 3c9f784f4962261f7624483ae4bd
4029a31f8e32)
    #15 0x70108c21c511  (/usr/lib/../lib/libSDL3.so.0+0x1c511) (BuildId: 3c9f784f4962261f7624483ae4bd4
029a31f8e32)
    #16 0x70109a403293  (/usr/lib/libSDL2-2.0.so.0+0x1a293) (BuildId: 70b531bd0eff55bb9a6cffca84c136d7
02321a2c)
    #17 0x605fa9634818 in game_init_sdl Video01/init_sdl.c:4
    #18 0x605fa96343ee in game_new Video01/game.c:18
    #19 0x605fa9634b00 in main Video01/main.c:8
    #20 0x701099a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75
a)
    #21 0x701099a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc1229
6052529af22f6a450a75a)
    #22 0x605fa9634204 in _start (/home/jeremiah/Tetris/C-SDL2/tetris+0x2204) (BuildId: b39dd191a269b3
185f6705dab0f2a65492e45aa9)

Indirect leak of 40 byte(s) in 1 object(s) allocated from:
    #0 0x701099cfd891 in malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x701098b5037a  (<unknown module>)
    #2 0x701098b40c56  (/home/jeremiah/Tetris/C-SDL2/tetris+0xdc56)
    #3 0x701098b42bbd  (/home/jeremiah/Tetris/C-SDL2/tetris+0xfbbd)
    #4 0x701098b4d8ce  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1a8ce)
    #5 0x701098b4dac7  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1aac7)
    #6 0x701098b4de20  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1ae20)
    #7 0x701098b4e3ac  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1b3ac)
    #8 0x701098b31e82  (<unknown module>)
    #9 0x701098b46b9f  (/home/jeremiah/Tetris/C-SDL2/tetris+0x13b9f)
    #10 0x701098b33d36  (<unknown module>)
    #11 0x701098b33fdd  (<unknown module>)
    #12 0x701098b342ca  (<unknown module>)
    #13 0x70108c3867b7  (/usr/lib/../lib/libSDL3.so.0+0x1867b7) (BuildId: 3c9f784f4962261f7624483ae4bd
4029a31f8e32)
    #14 0x70108c21c511  (/usr/lib/../lib/libSDL3.so.0+0x1c511) (BuildId: 3c9f784f4962261f7624483ae4bd4
029a31f8e32)
    #15 0x70109a403293  (/usr/lib/libSDL2-2.0.so.0+0x1a293) (BuildId: 70b531bd0eff55bb9a6cffca84c136d7
02321a2c)
    #16 0x605fa9634818 in game_init_sdl Video01/init_sdl.c:4
    #17 0x605fa96343ee in game_new Video01/game.c:18
    #18 0x605fa9634b00 in main Video01/main.c:8
    #19 0x701099a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75
a)
    #20 0x701099a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc1229
6052529af22f6a450a75a)
    #21 0x605fa9634204 in _start (/home/jeremiah/Tetris/C-SDL2/tetris+0x2204) (BuildId: b39dd191a269b3
185f6705dab0f2a65492e45aa9)

Indirect leak of 40 byte(s) in 1 object(s) allocated from:
    #0 0x701099cfd891 in malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x701098b5037a  (<unknown module>)
    #2 0x701098b40c56  (/home/jeremiah/Tetris/C-SDL2/tetris+0xdc56)
    #3 0x701098b42bbd  (/home/jeremiah/Tetris/C-SDL2/tetris+0xfbbd)
    #4 0x701098b4d8ce  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1a8ce)
    #5 0x701098b4dac7  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1aac7)
    #6 0x701098b4de20  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1ae20)
    #7 0x701098b4e3ac  (/home/jeremiah/Tetris/C-SDL2/tetris+0x1b3ac)
    #8 0x701098b31e82  (<unknown module>)
    #9 0x701098b46b9f  (/home/jeremiah/Tetris/C-SDL2/tetris+0x13b9f)
    #10 0x701098b33d36  (<unknown module>)
    #11 0x701098b33fdd  (<unknown module>)
    #12 0x701098b342ca  (<unknown module>)
    #13 0x70108c386786  (/usr/lib/../lib/libSDL3.so.0+0x186786) (BuildId: 3c9f784f4962261f7624483ae4bd
4029a31f8e32)
    #14 0x70108c21c511  (/usr/lib/../lib/libSDL3.so.0+0x1c511) (BuildId: 3c9f784f4962261f7624483ae4bd4
029a31f8e32)
    #15 0x70109a403293  (/usr/lib/libSDL2-2.0.so.0+0x1a293) (BuildId: 70b531bd0eff55bb9a6cffca84c136d7
02321a2c)
    #16 0x605fa9634818 in game_init_sdl Video01/init_sdl.c:4
    #17 0x605fa96343ee in game_new Video01/game.c:18
    #18 0x605fa9634b00 in main Video01/main.c:8
    #19 0x701099a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75
a)
    #20 0x701099a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc1229
6052529af22f6a450a75a)
    #21 0x605fa9634204 in _start (/home/jeremiah/Tetris/C-SDL2/tetris+0x2204) (BuildId: b39dd191a269b3
185f6705dab0f2a65492e45aa9)

Indirect leak of 24 byte(s) in 1 object(s) allocated from:
    #0 0x701099cfd891 in malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x701098b57498  (<unknown module>)
    #2 0x701098b3426e  (<unknown module>)
    #3 0x70108c386786  (/usr/lib/../lib/libSDL3.so.0+0x186786) (BuildId: 3c9f784f4962261f7624483ae4bd4
029a31f8e32)
    #4 0x70108c21c511  (/usr/lib/../lib/libSDL3.so.0+0x1c511) (BuildId: 3c9f784f4962261f7624483ae4bd40
29a31f8e32)
    #5 0x70109a403293  (/usr/lib/libSDL2-2.0.so.0+0x1a293) (BuildId: 70b531bd0eff55bb9a6cffca84c136d70
2321a2c)
    #6 0x605fa9634818 in game_init_sdl Video01/init_sdl.c:4
    #7 0x605fa96343ee in game_new Video01/game.c:18
    #8 0x605fa9634b00 in main Video01/main.c:8
    #9 0x701099a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a
)
    #10 0x701099a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc1229
6052529af22f6a450a75a)
    #11 0x605fa9634204 in _start (/home/jeremiah/Tetris/C-SDL2/tetris+0x2204) (BuildId: b39dd191a269b3
185f6705dab0f2a65492e45aa9)

Indirect leak of 24 byte(s) in 1 object(s) allocated from:
    #0 0x701099cfd891 in malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x701098b470c4  (/home/jeremiah/Tetris/C-SDL2/tetris+0x140c4)
    #2 0x70108c386766  (/usr/lib/../lib/libSDL3.so.0+0x186766) (BuildId: 3c9f784f4962261f7624483ae4bd4
029a31f8e32)
    #3 0x70108c21c511  (/usr/lib/../lib/libSDL3.so.0+0x1c511) (BuildId: 3c9f784f4962261f7624483ae4bd40
29a31f8e32)
    #4 0x70109a403293  (/usr/lib/libSDL2-2.0.so.0+0x1a293) (BuildId: 70b531bd0eff55bb9a6cffca84c136d70
2321a2c)
    #5 0x605fa9634818 in game_init_sdl Video01/init_sdl.c:4
    #6 0x605fa96343ee in game_new Video01/game.c:18
    #7 0x605fa9634b00 in main Video01/main.c:8
    #8 0x701099a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a
)
    #9 0x701099a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc12296
052529af22f6a450a75a)
    #10 0x605fa9634204 in _start (/home/jeremiah/Tetris/C-SDL2/tetris+0x2204) (BuildId: b39dd191a269b3
185f6705dab0f2a65492e45aa9)

SUMMARY: AddressSanitizer: 3381 byte(s) leaked in 35 allocation(s).
make: *** [Makefile:74: run] Error 1
```

## Comment 2621365368

other (NONE) · levaconline · 2025-01-29T11:18:22Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2621365368

https://github.com/libsdl-org/sdl2-compat/issues/254

## Comment 2621509578

reporter (NONE) · ProgrammingRainbow · 2025-01-29T12:29:01Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2621509578

I converted the above to SDL3 and checked ldd to see if it was linked to sdl3 shared object and it was and not linked with any sdl2 so. The sdl3 version create the same false memory leaks. So it's not just sdl2-compat it's also sdl3 that is having the issue. I understand sdl2-compat is using sdl3, which is why i checked it.

## Comment 2622572742

other (NONE) · christiansacks · 2025-01-29T18:55:02Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2622572742

**Issue with SyncTERM Input After Arch Update to sdl2-compat**

Hi,

I recently upgraded my Arch system, which replaced sdl2 with sdl2-compat, and I've encountered an issue with SyncTERM, an old-school BBS client. Prior to the update, everything worked as expected, but after switching to sdl2-compat, SyncTERM no longer sends key presses to the connected BBS.

I've reached out to the SyncTERM developer, and they're investigating whether something in sdl2-compat may be causing the issue. In the meantime, I wanted to check if this is something you're actively maintaining and, if so, what information you’d need from me to help debug the problem. Please let me know how I can assist in narrowing this down!

Thanks!

## Comment 2622578619

maintainer (COLLABORATOR) · slouken · 2025-01-29T18:57:50Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2622578619

> **Issue with SyncTERM Input After Arch Update to sdl2-compat**

I moved this to a new issue, for tracking.



## Comment 2622594462

maintainer (COLLABORATOR) · icculus · 2025-01-29T19:04:51Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2622594462

I pushed a fix for one leak that's in sdl2-compat itself, but almost all of these are under SDL_DBus_Init() in SDL3....rather, they are in libdbus, called into from SDL_DBus_Init().

But SDL2 does _not_ trigger all these, so SDL3 is legitimately leaking something somewhere.

I also get leaks in Nvidia's drivers that SDL2 doesn't trigger, so let's make sure we didn't, like, fail to delete the GL context in SDL_DestroyRenderer, too. This is also an SDL3 thing, not sdl2-compat.

## Comment 2624624195

reporter (NONE) · ProgrammingRainbow · 2025-01-30T14:11:29Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2624624195

I opened an issue on Archlinux sdl2-compat asking for sdl2 to brought back at least as an option.

https://gitlab.archlinux.org/archlinux/packaging/packages/sdl2-compat/-/issues/1

## Comment 2624668819

maintainer (COLLABORATOR) · icculus · 2025-01-30T14:30:03Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2624668819

Arch can do what it wants, but it's a small, one-time memory leak that we'll probably fix shortly.

## Comment 2624950250

reporter (NONE) · ProgrammingRainbow · 2025-01-30T16:19:20Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2624950250

I was simply giving info since most of the current bug reports are from arch users who got rug pulled. There working package got replaced with something that doesn't. And there is an influx of people looking for information and help. The issue i raised was bringing back the working package and having this as an alternative since it's not ready to use yet.

## Comment 2626455020

maintainer (COLLABORATOR) · icculus · 2025-01-31T07:09:00Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2626455020

More notes on memory leaks:

We call XrmInitialize() in the X11 backend, which allocates memory it never frees behind our backs.

https://github.com/ghaerr/nxlib/blob/68f61d915b28f00ceaa97301bd5a2c0fb7258f12/Xrm.c#L323-L327

This eventually ends up in a variable they call "neverFreeTable".  :/

https://github.com/ghaerr/nxlib/blob/e190e2080ad4808056d2ba208d008f1a25bd4d28/Quarks.c#L108-L129

We probably can't do anything about that except move to Wayland.

It's possible that the reason we're using this (DPI detection) isn't necessary or reliable, and we can just scrap it if so:

https://github.com/libsdl-org/SDL/blob/43924ec87325c32b5c60d8bc22087d1d77efcacd/src/video/x11/SDL_x11modes.c#L64-L89


(But again, this is a small leak that happens once at startup, not a massive ongoing bloating of address space.)


We also call XSetLocaleModifiers("") and this leaks in a similar way. There doesn't appear to be a way to reset it, and you have to call this function or things will go wrong (according to the manpage).


These are Xlib allocations; maybe moving to xcb would allow us to avoid them, but I don't know the details and doing that would be a massive destabilization of our X11 support.



The D-Bus leaks are easy: if I export SDL_SHUTDOWN_DBUS_ON_QUIT=1, they go away. We close and deref the D-Bus objects we own, but we don't actually call dbus_shutdown() without that hint, which defaults to false. We unload the D-Bus library no matter what though. I sort of think this hint should default to true; apps that are _also_ using D-Bus outside of SDL should set it explicitly, since they're going to be a minority (and someone should probably file a bug with D-Bus about this interface, too.)



## Comment 2626455746

maintainer (COLLABORATOR) · icculus · 2025-01-31T07:09:39Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2626455746

Anyhow, tl;dr: (stop using X11 and then) export SDL_VIDEO_DRIVER=wayland and SDL_SHUTDOWN_DBUS_ON_QUIT=1 and AddressSanitizer will (probably) find zero leaks.

## Comment 2627716373

reporter (NONE) · ProgrammingRainbow · 2025-01-31T16:13:43Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2627716373

Yeah stop using x11 doesn't sound like a real answer. Unless your going to tell people that sdl3 no longer supports X11. But it sounds like you have some memory leaks that need to be addressed. There is a function that shuts down sdl called SDL_Quit this should be freeing any memory that SDL has allocated. If it's not then you have a bug there. Telling people to not use X11 because you have memory likes is like a doctor telling the patient not to press there because it will hurt. Instead of addressing the issue. There is a lot of projects that are using sdl2 and also using x11. So if sdl3 is broken or doesn't support actual sdl2 code or x11 then sdl2-compat should not really exist since it's not actually targeting the actual sdl2 use case. By the way does xmonad support wayland now? Since Xmonad is my primary desktop. Also does ffmpeg support wayland now? Think it doesn't.

## Comment 2627761111

maintainer (COLLABORATOR) · icculus · 2025-01-31T16:33:10Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2627761111

Sorry, I was being glib. The "stop using x11" comment was obviously not intended to be a real solution.

But I can't free memory I didn't allocate and don't even have a pointer to. A decades-old library is doing it and offers no way to free it, intentionally, other than terminating the process.

The D-Bus thing is tricky, too, because the way you fix the leak is to call a global shutdown function that will break anything else in the app using D-Bus outside of SDL. Again, this is not our code. I'm of the opinion we should take the crash risk here, because it's an uncommon situation, but that's to be decided still.

## Comment 2627779708

maintainer (COLLABORATOR) · slouken · 2025-01-31T16:42:24Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2627779708

From the D-Bus documentation:
> You MUST free all memory and release all reference counts returned to you by libdbus prior to calling [dbus_shutdown()](https://dbus.freedesktop.org/doc/api/html/group__DBusMemory.html#ga01912903e39428872920d861ef565bac).
> 
> If a shared connection is open, calling [dbus_shutdown()](https://dbus.freedesktop.org/doc/api/html/group__DBusMemory.html#ga01912903e39428872920d861ef565bac) will drain its queue of messages and disconnect it. In particular, this will result in processing of the special Disconnected signal, which may result in a call to _exit(), unless you have used [dbus_connection_set_exit_on_disconnect()](https://dbus.freedesktop.org/doc/api/html/group__DBusConnection.html#ga19091beb74f1504b0e862a7ad10e71cd) to disable that behaviour.
> 
> You can't continue to use any D-Bus objects, such as connections, that were allocated prior to [dbus_shutdown()](https://dbus.freedesktop.org/doc/api/html/group__DBusMemory.html#ga01912903e39428872920d861ef565bac). You can, however, start over; call [dbus_threads_init()](https://dbus.freedesktop.org/doc/api/html/group__DBusThreads.html#gac7b8a7001befc3eaa8c6b043151008dc) again, create new connections, and so forth.
> 
> WARNING: [dbus_shutdown()](https://dbus.freedesktop.org/doc/api/html/group__DBusMemory.html#ga01912903e39428872920d861ef565bac) is NOT thread safe, it must be called while NO other threads are using D-Bus. (Remember, you have to free all D-Bus objects and memory before you call [dbus_shutdown()](https://dbus.freedesktop.org/doc/api/html/group__DBusMemory.html#ga01912903e39428872920d861ef565bac), so no thread can be using libdbus.)
> 
> The purpose of [dbus_shutdown()](https://dbus.freedesktop.org/doc/api/html/group__DBusMemory.html#ga01912903e39428872920d861ef565bac) is to allow applications to get clean output from memory leak checkers. [dbus_shutdown()](https://dbus.freedesktop.org/doc/api/html/group__DBusMemory.html#ga01912903e39428872920d861ef565bac) may also be useful if you want to dlopen() libdbus instead of linking to it, and want to be able to unload the library again.
> 
> There is absolutely no requirement to call [dbus_shutdown()](https://dbus.freedesktop.org/doc/api/html/group__DBusMemory.html#ga01912903e39428872920d861ef565bac) - in fact, most applications won't bother and should not feel guilty.
> 
> You have to know that nobody is using libdbus in your application's process before you can call [dbus_shutdown()](https://dbus.freedesktop.org/doc/api/html/group__DBusMemory.html#ga01912903e39428872920d861ef565bac). One implication of this is that **calling [dbus_shutdown()](https://dbus.freedesktop.org/doc/api/html/group__DBusMemory.html#ga01912903e39428872920d861ef565bac) from a library is almost certainly wrong**, since you don't know what the rest of the app is up to.

This is pretty clear that we shouldn't do this by default and that SDL_SHUTDOWN_DBUS_ON_QUIT should only be set by people trying to do memory leak detection.

## Comment 2627812302

reporter (NONE) · ProgrammingRainbow · 2025-01-31T16:59:18Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2627812302

Sorry i read that dbus as you must call it after releasing all memory. So it should be called by SDL_Quit()

So lets check out your suggestions for the best case.

## My Yellow-Snow game which doesn't produce any memory leaks in Wayland/X11 at all for sdl2. in Wayland with the dbus switch in sdl2-compat it's a different story.

SDL_VIDEO_DRIVER=wayland SDL_SHUTDOWN_DBUS_ON_QUIT=1 make rebuild run
```
=================================================================
==2879==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 10775 byte(s) in 1 object(s) allocated from:
    #0 0x73d3dbefd891 in malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x73d3ce4c124e  (/usr/lib/../lib/libSDL3.so.0+0xc124e) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #2 0x73d3dc65445e  (/usr/lib/libSDL2_ttf-2.0.so.0+0x345e) (BuildId: abb54ecb46850356af219dd446d878f8b8755ff5)
    #3 0x73d3dc654a73  (/usr/lib/libSDL2_ttf-2.0.so.0+0x3a73) (BuildId: abb54ecb46850356af219dd446d878f8b8755ff5)
    #4 0x73d3dc65f94d  (/usr/lib/libSDL2_ttf-2.0.so.0+0xe94d) (BuildId: abb54ecb46850356af219dd446d878f8b8755ff5)
    #5 0x5816ce09aaae in score_update /home/jeremiah/Yellow-Snow/C-SDL2/score.c:61
    #6 0x5816ce09a883 in score_reset /home/jeremiah/Yellow-Snow/C-SDL2/score.c:45
    #7 0x5816ce09a660 in score_new /home/jeremiah/Yellow-Snow/C-SDL2/score.c:24
    #8 0x5816ce097a49 in game_new /home/jeremiah/Yellow-Snow/C-SDL2/game.c:37
    #9 0x5816ce099560 in main /home/jeremiah/Yellow-Snow/C-SDL2/main.c:9
    #10 0x73d3dbc34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #11 0x73d3dbc34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #12 0x5816ce096414 in _start (/home/jeremiah/Yellow-Snow/C-SDL2/yellow-snow+0x3414) (BuildId: d7d32dad4054c73bd3bca90bb45f971f7debaffe)

Direct leak of 2696 byte(s) in 1 object(s) allocated from:
    #0 0x73d3dbefd1aa in calloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x73d3cf371dcf  (<unknown module>)
    #2 0x73d3cf3724ef  (<unknown module>)
    #3 0x73d3d0bd08f4  (<unknown module>)

Direct leak of 256 byte(s) in 1 object(s) allocated from:
    #0 0x73d3dbefc542 in realloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:85
    #1 0x73d3c86e058c  (<unknown module>)
    #2 0x73d3c86e0a50  (<unknown module>)
    #3 0x73d3dbca883a  (/usr/lib/libc.so.6+0x9983a) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #4 0x73d3dbca88b8 in __pthread_once (/usr/lib/libc.so.6+0x998b8) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #5 0x73d3c8b22f9f  (<unknown module>)
    #6 0x73d3c8bddb6d  (<unknown module>)
    #7 0x73d3c8b23268  (<unknown module>)
    #8 0x73d3c8232eb2  (<unknown module>)
    #9 0x73d3c89b13af  (<unknown module>)
    #10 0x73d3c82371d3  (<unknown module>)
    #11 0x73d3cf377ce9  (<unknown module>)
    #12 0x73d3cf38260f  (<unknown module>)
    #13 0x73d3cf378608  (<unknown module>)
    #14 0x73d3cf36694b  (<unknown module>)
    #15 0x73d3ce506e31  (/usr/lib/../lib/libSDL3.so.0+0x106e31) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #16 0x73d3ce570329  (/usr/lib/../lib/libSDL3.so.0+0x170329) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #17 0x73d3ce51c852  (/usr/lib/../lib/libSDL3.so.0+0x11c852) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #18 0x73d3ce522b2e  (/usr/lib/../lib/libSDL3.so.0+0x122b2e) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #19 0x73d3ce491cd1  (/usr/lib/../lib/libSDL3.so.0+0x91cd1) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #20 0x73d3ce4805d5  (/usr/lib/../lib/libSDL3.so.0+0x805d5) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #21 0x73d3ce4807d6  (/usr/lib/../lib/libSDL3.so.0+0x807d6) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #22 0x73d3dc5dceeb  (/usr/lib/libSDL2-2.0.so.0+0x18eeb) (BuildId: 328f55c57f6d6eade54cd90ed4dbcd155e1eedb5)
    #23 0x5816ce098cd6 in game_initilize /home/jeremiah/Yellow-Snow/C-SDL2/initialize.c:33
    #24 0x5816ce09782c in game_new /home/jeremiah/Yellow-Snow/C-SDL2/game.c:13
    #25 0x5816ce099560 in main /home/jeremiah/Yellow-Snow/C-SDL2/main.c:9
    #26 0x73d3dbc34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #27 0x73d3dbc34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #28 0x5816ce096414 in _start (/home/jeremiah/Yellow-Snow/C-SDL2/yellow-snow+0x3414) (BuildId: d7d32dad4054c73bd3bca90bb45f971f7debaffe)

Direct leak of 96 byte(s) in 1 object(s) allocated from:
    #0 0x73d3dbefd1aa in calloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x73d3dad334de  (<unknown module>)
    #2 0x73d3dad34193  (<unknown module>)
    #3 0x73d3dad354cb  (<unknown module>)
    #4 0x73d3ce579055  (/usr/lib/../lib/libSDL3.so.0+0x179055) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #5 0x73d3ce41d4fd  (/usr/lib/../lib/libSDL3.so.0+0x1d4fd) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #6 0x73d3dc5de393  (/usr/lib/libSDL2-2.0.so.0+0x1a393) (BuildId: 328f55c57f6d6eade54cd90ed4dbcd155e1eedb5)
    #7 0x5816ce098a37 in game_initilize /home/jeremiah/Yellow-Snow/C-SDL2/initialize.c:5
    #8 0x5816ce09782c in game_new /home/jeremiah/Yellow-Snow/C-SDL2/game.c:13
    #9 0x5816ce099560 in main /home/jeremiah/Yellow-Snow/C-SDL2/main.c:9
    #10 0x73d3dbc34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #11 0x73d3dbc34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #12 0x5816ce096414 in _start (/home/jeremiah/Yellow-Snow/C-SDL2/yellow-snow+0x3414) (BuildId: d7d32dad4054c73bd3bca90bb45f971f7debaffe)

Indirect leak of 144 byte(s) in 1 object(s) allocated from:
    #0 0x73d3dbefd1aa in calloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x73d3cf10d8c7  (<unknown module>)
    #2 0x73d3cf10dc53  (<unknown module>)
    #3 0x73d3cf112921  (<unknown module>)
    #4 0x73d3cf3717eb  (<unknown module>)
    #5 0x73d3cf366840  (<unknown module>)
    #6 0x73d3ce506e31  (/usr/lib/../lib/libSDL3.so.0+0x106e31) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #7 0x73d3ce570329  (/usr/lib/../lib/libSDL3.so.0+0x170329) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #8 0x73d3ce51c852  (/usr/lib/../lib/libSDL3.so.0+0x11c852) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #9 0x73d3ce522b2e  (/usr/lib/../lib/libSDL3.so.0+0x122b2e) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #10 0x73d3ce491cd1  (/usr/lib/../lib/libSDL3.so.0+0x91cd1) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #11 0x73d3ce4805d5  (/usr/lib/../lib/libSDL3.so.0+0x805d5) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #12 0x73d3ce4807d6  (/usr/lib/../lib/libSDL3.so.0+0x807d6) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #13 0x73d3dc5dceeb  (/usr/lib/libSDL2-2.0.so.0+0x18eeb) (BuildId: 328f55c57f6d6eade54cd90ed4dbcd155e1eedb5)
    #14 0x5816ce098cd6 in game_initilize /home/jeremiah/Yellow-Snow/C-SDL2/initialize.c:33
    #15 0x5816ce09782c in game_new /home/jeremiah/Yellow-Snow/C-SDL2/game.c:13
    #16 0x5816ce099560 in main /home/jeremiah/Yellow-Snow/C-SDL2/main.c:9
    #17 0x73d3dbc34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #18 0x73d3dbc34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #19 0x5816ce096414 in _start (/home/jeremiah/Yellow-Snow/C-SDL2/yellow-snow+0x3414) (BuildId: d7d32dad4054c73bd3bca90bb45f971f7debaffe)

Indirect leak of 40 byte(s) in 1 object(s) allocated from:
    #0 0x73d3dbefd1aa in calloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x73d3cf37185f  (<unknown module>)
    #2 0x73d3cf366840  (<unknown module>)
    #3 0x73d3ce506e31  (/usr/lib/../lib/libSDL3.so.0+0x106e31) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #4 0x73d3ce570329  (/usr/lib/../lib/libSDL3.so.0+0x170329) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #5 0x73d3ce51c852  (/usr/lib/../lib/libSDL3.so.0+0x11c852) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #6 0x73d3ce522b2e  (/usr/lib/../lib/libSDL3.so.0+0x122b2e) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #7 0x73d3ce491cd1  (/usr/lib/../lib/libSDL3.so.0+0x91cd1) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #8 0x73d3ce4805d5  (/usr/lib/../lib/libSDL3.so.0+0x805d5) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #9 0x73d3ce4807d6  (/usr/lib/../lib/libSDL3.so.0+0x807d6) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #10 0x73d3dc5dceeb  (/usr/lib/libSDL2-2.0.so.0+0x18eeb) (BuildId: 328f55c57f6d6eade54cd90ed4dbcd155e1eedb5)
    #11 0x5816ce098cd6 in game_initilize /home/jeremiah/Yellow-Snow/C-SDL2/initialize.c:33
    #12 0x5816ce09782c in game_new /home/jeremiah/Yellow-Snow/C-SDL2/game.c:13
    #13 0x5816ce099560 in main /home/jeremiah/Yellow-Snow/C-SDL2/main.c:9
    #14 0x73d3dbc34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #15 0x73d3dbc34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #16 0x5816ce096414 in _start (/home/jeremiah/Yellow-Snow/C-SDL2/yellow-snow+0x3414) (BuildId: d7d32dad4054c73bd3bca90bb45f971f7debaffe)

SUMMARY: AddressSanitizer: 14007 byte(s) leaked in 6 allocation(s).
```

## Conways Game of Life written in both C and Cpp. sdl2 no issues. in sdl2-compat

SDL_VIDEO_DRIVER=wayland SDL_SHUTDOWN_DBUS_ON_QUIT=1 make rebuild run
```
=================================================================
==3150==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 20087 byte(s) in 1 object(s) allocated from:
    #0 0x7374b40fd891 in malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x7374a64c124e  (/usr/lib/../lib/libSDL3.so.0+0xc124e) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #2 0x7374b475945e  (/usr/lib/libSDL2_ttf-2.0.so.0+0x345e) (BuildId: abb54ecb46850356af219dd446d878f8b8755ff5)
    #3 0x7374b4759a73  (/usr/lib/libSDL2_ttf-2.0.so.0+0x3a73) (BuildId: abb54ecb46850356af219dd446d878f8b8755ff5)
    #4 0x7374b476494d  (/usr/lib/libSDL2_ttf-2.0.so.0+0xe94d) (BuildId: abb54ecb46850356af219dd446d878f8b8755ff5)
    #5 0x560fa93eebda in Message::update(bool, double) src/message.cpp:25
    #6 0x560fa93ee841 in Message::init(bool, double) src/message.cpp:10
    #7 0x560fa93a5ba5 in Game::init() src/game.cpp:27
    #8 0x560fa93ebc9e in main src/main.cpp:6
    #9 0x7374b3a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #10 0x7374b3a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #11 0x560fa939f7d4 in _start (/home/jeremiah/Conways-Game-of-Life-Cpp-SDL2/game-of-life+0x157d4) (BuildId: 16f80fcd58d3b252fd937b313b011631f8a61ea5)

Direct leak of 2696 byte(s) in 1 object(s) allocated from:
    #0 0x7374b40fd1aa in calloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x7374a8d3ddcf  (<unknown module>)
    #2 0x7374a8d3e4ef  (<unknown module>)
    #3 0x7374a8fce8f4  (/usr/lib/libstdc++.so.6.0.33+0x14d38f4)

Direct leak of 256 byte(s) in 1 object(s) allocated from:
    #0 0x7374b40fc542 in realloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:85
    #1 0x7374a2ce058c  (<unknown module>)
    #2 0x7374a2ce0a50  (<unknown module>)
    #3 0x7374b3aa883a  (/usr/lib/libc.so.6+0x9983a) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #4 0x7374b3aa88b8 in __pthread_once (/usr/lib/libc.so.6+0x998b8) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #5 0x7374a3122f9f  (<unknown module>)
    #6 0x7374a31ddb6d  (/usr/lib/libLLVM.so.19.1+0x1ddb6d)
    #7 0x7374a3123268  (<unknown module>)
    #8 0x7374a2832eb2  (<unknown module>)
    #9 0x7374a2fb13af  (<unknown module>)
    #10 0x7374a28371d3  (<unknown module>)
    #11 0x7374a8d43ce9  (<unknown module>)
    #12 0x7374a8d4e60f  (<unknown module>)
    #13 0x7374a8d44608  (<unknown module>)
    #14 0x7374a8d3294b  (<unknown module>)
    #15 0x7374a6506e31  (/usr/lib/../lib/libSDL3.so.0+0x106e31) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #16 0x7374a6570329  (/usr/lib/../lib/libSDL3.so.0+0x170329) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #17 0x7374a651c852  (/usr/lib/../lib/libSDL3.so.0+0x11c852) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #18 0x7374a6522b2e  (/usr/lib/../lib/libSDL3.so.0+0x122b2e) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #19 0x7374a6491cd1  (/usr/lib/../lib/libSDL3.so.0+0x91cd1) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #20 0x7374a64805d5  (/usr/lib/../lib/libSDL3.so.0+0x805d5) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #21 0x7374a64807d6  (/usr/lib/../lib/libSDL3.so.0+0x807d6) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #22 0x7374b4713eeb  (/usr/lib/libSDL2-2.0.so.0+0x18eeb) (BuildId: 328f55c57f6d6eade54cd90ed4dbcd155e1eedb5)
    #23 0x560fa93afc62 in Game::init_sdl() src/init_sdl.cpp:31
    #24 0x560fa93a59c0 in Game::init() src/game.cpp:19
    #25 0x560fa93ebc9e in main src/main.cpp:6
    #26 0x7374b3a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #27 0x7374b3a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #28 0x560fa939f7d4 in _start (/home/jeremiah/Conways-Game-of-Life-Cpp-SDL2/game-of-life+0x157d4) (BuildId: 16f80fcd58d3b252fd937b313b011631f8a61ea5)

Direct leak of 96 byte(s) in 1 object(s) allocated from:
    #0 0x7374b40fd1aa in calloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x7374b29054de  (<unknown module>)
    #2 0x7374b2906193  (<unknown module>)
    #3 0x7374b29074cb  (<unknown module>)
    #4 0x7374a6579055  (/usr/lib/../lib/libSDL3.so.0+0x179055) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #5 0x7374a641d4fd  (/usr/lib/../lib/libSDL3.so.0+0x1d4fd) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #6 0x7374b4715393  (/usr/lib/libSDL2-2.0.so.0+0x1a393) (BuildId: 328f55c57f6d6eade54cd90ed4dbcd155e1eedb5)
    #7 0x560fa93af815 in Game::init_sdl() src/init_sdl.cpp:4
    #8 0x560fa93a59c0 in Game::init() src/game.cpp:19
    #9 0x560fa93ebc9e in main src/main.cpp:6
    #10 0x7374b3a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #11 0x7374b3a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #12 0x560fa939f7d4 in _start (/home/jeremiah/Conways-Game-of-Life-Cpp-SDL2/game-of-life+0x157d4) (BuildId: 16f80fcd58d3b252fd937b313b011631f8a61ea5)

Indirect leak of 144 byte(s) in 1 object(s) allocated from:
    #0 0x7374b40fd1aa in calloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x7374a8d068c7  (<unknown module>)
    #2 0x7374a8d06c53  (<unknown module>)
    #3 0x7374a8d0b921  (<unknown module>)
    #4 0x7374a8d3d7eb  (<unknown module>)
    #5 0x7374a8d32840  (<unknown module>)
    #6 0x7374a6506e31  (/usr/lib/../lib/libSDL3.so.0+0x106e31) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #7 0x7374a6570329  (/usr/lib/../lib/libSDL3.so.0+0x170329) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #8 0x7374a651c852  (/usr/lib/../lib/libSDL3.so.0+0x11c852) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #9 0x7374a6522b2e  (/usr/lib/../lib/libSDL3.so.0+0x122b2e) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #10 0x7374a6491cd1  (/usr/lib/../lib/libSDL3.so.0+0x91cd1) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #11 0x7374a64805d5  (/usr/lib/../lib/libSDL3.so.0+0x805d5) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #12 0x7374a64807d6  (/usr/lib/../lib/libSDL3.so.0+0x807d6) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #13 0x7374b4713eeb  (/usr/lib/libSDL2-2.0.so.0+0x18eeb) (BuildId: 328f55c57f6d6eade54cd90ed4dbcd155e1eedb5)
    #14 0x560fa93afc62 in Game::init_sdl() src/init_sdl.cpp:31
    #15 0x560fa93a59c0 in Game::init() src/game.cpp:19
    #16 0x560fa93ebc9e in main src/main.cpp:6
    #17 0x7374b3a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #18 0x7374b3a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #19 0x560fa939f7d4 in _start (/home/jeremiah/Conways-Game-of-Life-Cpp-SDL2/game-of-life+0x157d4) (BuildId: 16f80fcd58d3b252fd937b313b011631f8a61ea5)

Indirect leak of 40 byte(s) in 1 object(s) allocated from:
    #0 0x7374b40fd1aa in calloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x7374a8d3d85f  (<unknown module>)
    #2 0x7374a8d32840  (<unknown module>)
    #3 0x7374a6506e31  (/usr/lib/../lib/libSDL3.so.0+0x106e31) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #4 0x7374a6570329  (/usr/lib/../lib/libSDL3.so.0+0x170329) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #5 0x7374a651c852  (/usr/lib/../lib/libSDL3.so.0+0x11c852) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #6 0x7374a6522b2e  (/usr/lib/../lib/libSDL3.so.0+0x122b2e) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #7 0x7374a6491cd1  (/usr/lib/../lib/libSDL3.so.0+0x91cd1) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #8 0x7374a64805d5  (/usr/lib/../lib/libSDL3.so.0+0x805d5) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #9 0x7374a64807d6  (/usr/lib/../lib/libSDL3.so.0+0x807d6) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #10 0x7374b4713eeb  (/usr/lib/libSDL2-2.0.so.0+0x18eeb) (BuildId: 328f55c57f6d6eade54cd90ed4dbcd155e1eedb5)
    #11 0x560fa93afc62 in Game::init_sdl() src/init_sdl.cpp:31
    #12 0x560fa93a59c0 in Game::init() src/game.cpp:19
    #13 0x560fa93ebc9e in main src/main.cpp:6
    #14 0x7374b3a34e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #15 0x7374b3a34ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #16 0x560fa939f7d4 in _start (/home/jeremiah/Conways-Game-of-Life-Cpp-SDL2/game-of-life+0x157d4) (BuildId: 16f80fcd58d3b252fd937b313b011631f8a61ea5)

SUMMARY: AddressSanitizer: 23319 byte(s) leaked in 6 allocation(s).

```

## Minesweeper again written in both C and C++

SDL_VIDEO_DRIVER=wayland SDL_SHUTDOWN_DBUS_ON_QUIT=1 make rebuild run
```
=================================================================
==3310==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 2696 byte(s) in 1 object(s) allocated from:
    #0 0x7d75eeafd1aa in calloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x7d75e3d3ddcf  (<unknown module>)
    #2 0x7d75e3d3e4ef  (<unknown module>)
    #3 0x7d75e410e8f4  (<unknown module>)

Direct leak of 256 byte(s) in 1 object(s) allocated from:
    #0 0x7d75eeafc542 in realloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:85
    #1 0x7d75ddae058c  (<unknown module>)
    #2 0x7d75ddae0a50  (<unknown module>)
    #3 0x7d75ee8a883a  (/usr/lib/libc.so.6+0x9983a) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #4 0x7d75ee8a88b8 in __pthread_once (/usr/lib/libc.so.6+0x998b8) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #5 0x7d75ddf22f9f  (<unknown module>)
    #6 0x7d75ddfddb6d  (<unknown module>)
    #7 0x7d75ddf23268  (<unknown module>)
    #8 0x7d75dd632eb2  (<unknown module>)
    #9 0x7d75dddb13af  (<unknown module>)
    #10 0x7d75dd6371d3  (<unknown module>)
    #11 0x7d75e3d43ce9  (<unknown module>)
    #12 0x7d75e3d4e60f  (<unknown module>)
    #13 0x7d75e3d44608  (<unknown module>)
    #14 0x7d75e3d3294b  (<unknown module>)
    #15 0x7d75e1306e31  (/usr/lib/../lib/libSDL3.so.0+0x106e31) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #16 0x7d75e1370329  (/usr/lib/../lib/libSDL3.so.0+0x170329) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #17 0x7d75e131c852  (/usr/lib/../lib/libSDL3.so.0+0x11c852) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #18 0x7d75e1322b2e  (/usr/lib/../lib/libSDL3.so.0+0x122b2e) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #19 0x7d75e1291cd1  (/usr/lib/../lib/libSDL3.so.0+0x91cd1) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #20 0x7d75e12805d5  (/usr/lib/../lib/libSDL3.so.0+0x805d5) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #21 0x7d75e12807d6  (/usr/lib/../lib/libSDL3.so.0+0x807d6) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #22 0x7d75ef242eeb  (/usr/lib/libSDL2-2.0.so.0+0x18eeb) (BuildId: 328f55c57f6d6eade54cd90ed4dbcd155e1eedb5)
    #23 0x608f1e9491f0 in game_init_sdl src/init_sdl.c:23
    #24 0x608f1e946707 in game_new src/game.c:36
    #25 0x608f1e949a02 in main src/main.c:8
    #26 0x7d75ee834e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #27 0x7d75ee834ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #28 0x608f1e93d314 in _start (/home/jeremiah/Minesweeper/C-SDL2/minesweeper+0x3314) (BuildId: 6d5a61d6418488d794fa6ac18dc96ed1618441a3)

Direct leak of 96 byte(s) in 1 object(s) allocated from:
    #0 0x7d75eeafd1aa in calloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x7d75edb774de  (<unknown module>)
    #2 0x7d75edb78193  (<unknown module>)
    #3 0x7d75edb794cb  (<unknown module>)
    #4 0x7d75e1379055  (/usr/lib/../lib/libSDL3.so.0+0x179055) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #5 0x7d75e121d4fd  (/usr/lib/../lib/libSDL3.so.0+0x1d4fd) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #6 0x7d75ef244393  (/usr/lib/libSDL2-2.0.so.0+0x1a393) (BuildId: 328f55c57f6d6eade54cd90ed4dbcd155e1eedb5)
    #7 0x608f1e94902d in game_init_sdl src/init_sdl.c:4
    #8 0x608f1e946707 in game_new src/game.c:36
    #9 0x608f1e949a02 in main src/main.c:8
    #10 0x7d75ee834e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #11 0x7d75ee834ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #12 0x608f1e93d314 in _start (/home/jeremiah/Minesweeper/C-SDL2/minesweeper+0x3314) (BuildId: 6d5a61d6418488d794fa6ac18dc96ed1618441a3)

Indirect leak of 144 byte(s) in 1 object(s) allocated from:
    #0 0x7d75eeafd1aa in calloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x7d75e3d068c7  (<unknown module>)
    #2 0x7d75e3d06c53  (<unknown module>)
    #3 0x7d75e3d0b921  (<unknown module>)
    #4 0x7d75e3d3d7eb  (<unknown module>)
    #5 0x7d75e3d32840  (<unknown module>)
    #6 0x7d75e1306e31  (/usr/lib/../lib/libSDL3.so.0+0x106e31) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #7 0x7d75e1370329  (/usr/lib/../lib/libSDL3.so.0+0x170329) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #8 0x7d75e131c852  (/usr/lib/../lib/libSDL3.so.0+0x11c852) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #9 0x7d75e1322b2e  (/usr/lib/../lib/libSDL3.so.0+0x122b2e) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #10 0x7d75e1291cd1  (/usr/lib/../lib/libSDL3.so.0+0x91cd1) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #11 0x7d75e12805d5  (/usr/lib/../lib/libSDL3.so.0+0x805d5) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #12 0x7d75e12807d6  (/usr/lib/../lib/libSDL3.so.0+0x807d6) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #13 0x7d75ef242eeb  (/usr/lib/libSDL2-2.0.so.0+0x18eeb) (BuildId: 328f55c57f6d6eade54cd90ed4dbcd155e1eedb5)
    #14 0x608f1e9491f0 in game_init_sdl src/init_sdl.c:23
    #15 0x608f1e946707 in game_new src/game.c:36
    #16 0x608f1e949a02 in main src/main.c:8
    #17 0x7d75ee834e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #18 0x7d75ee834ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #19 0x608f1e93d314 in _start (/home/jeremiah/Minesweeper/C-SDL2/minesweeper+0x3314) (BuildId: 6d5a61d6418488d794fa6ac18dc96ed1618441a3)

Indirect leak of 40 byte(s) in 1 object(s) allocated from:
    #0 0x7d75eeafd1aa in calloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x7d75e3d3d85f  (<unknown module>)
    #2 0x7d75e3d32840  (<unknown module>)
    #3 0x7d75e1306e31  (/usr/lib/../lib/libSDL3.so.0+0x106e31) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #4 0x7d75e1370329  (/usr/lib/../lib/libSDL3.so.0+0x170329) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #5 0x7d75e131c852  (/usr/lib/../lib/libSDL3.so.0+0x11c852) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #6 0x7d75e1322b2e  (/usr/lib/../lib/libSDL3.so.0+0x122b2e) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #7 0x7d75e1291cd1  (/usr/lib/../lib/libSDL3.so.0+0x91cd1) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #8 0x7d75e12805d5  (/usr/lib/../lib/libSDL3.so.0+0x805d5) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #9 0x7d75e12807d6  (/usr/lib/../lib/libSDL3.so.0+0x807d6) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #10 0x7d75ef242eeb  (/usr/lib/libSDL2-2.0.so.0+0x18eeb) (BuildId: 328f55c57f6d6eade54cd90ed4dbcd155e1eedb5)
    #11 0x608f1e9491f0 in game_init_sdl src/init_sdl.c:23
    #12 0x608f1e946707 in game_new src/game.c:36
    #13 0x608f1e949a02 in main src/main.c:8
    #14 0x7d75ee834e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #15 0x7d75ee834ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #16 0x608f1e93d314 in _start (/home/jeremiah/Minesweeper/C-SDL2/minesweeper+0x3314) (BuildId: 6d5a61d6418488d794fa6ac18dc96ed1618441a3)

SUMMARY: AddressSanitizer: 3232 byte(s) leaked in 5 allocation(s).
```

## How about an SDL3 application? Beginners Guide to SDL3 in C and also the Cpp version does the same.

SDL_VIDEO_DRIVER=wayland SDL_SHUTDOWN_DBUS_ON_QUIT=1 make clean debug run
```
=================================================================
==3423==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 2696 byte(s) in 1 object(s) allocated from:
    #0 0x74114d6fd1aa in calloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x741145d64dcf  (<unknown module>)
    #2 0x741145d654ef  (<unknown module>)
    #3 0x74114a3a28f4  (/usr/lib/debug/usr/lib/libSDL3_mixer.so.0.0.0.debug+0x918f4)

Direct leak of 256 byte(s) in 1 object(s) allocated from:
    #0 0x74114d6fc542 in realloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:85
    #1 0x7411438e058c  (<unknown module>)
    #2 0x7411438e0a50  (<unknown module>)
    #3 0x74114d0a883a  (/usr/lib/libc.so.6+0x9983a) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #4 0x74114d0a88b8 in __pthread_once (/usr/lib/libc.so.6+0x998b8) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #5 0x741143d22f9f  (<unknown module>)
    #6 0x741143dddb6d  (<unknown module>)
    #7 0x741143d23268  (<unknown module>)
    #8 0x741143432eb2  (<unknown module>)
    #9 0x741143bb13af  (<unknown module>)
    #10 0x7411434371d3  (<unknown module>)
    #11 0x741145d6ace9  (<unknown module>)
    #12 0x741145d7560f  (<unknown module>)
    #13 0x741145d6b608  (<unknown module>)
    #14 0x741145d5994b  (<unknown module>)
    #15 0x74114d306e31  (/usr/lib/libSDL3.so.0+0x106e31) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #16 0x74114d370329  (/usr/lib/libSDL3.so.0+0x170329) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #17 0x74114d31c852  (/usr/lib/libSDL3.so.0+0x11c852) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #18 0x74114d322b2e  (/usr/lib/libSDL3.so.0+0x122b2e) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #19 0x74114d291cd1  (/usr/lib/libSDL3.so.0+0x91cd1) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #20 0x74114d2805d5  (/usr/lib/libSDL3.so.0+0x805d5) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #21 0x74114d2807d6  (/usr/lib/libSDL3.so.0+0x807d6) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #22 0x5d79ec82f8cb in game_init_sdl src/main.c:90
    #23 0x5d79ec83040f in game_new src/main.c:174
    #24 0x5d79ec831994 in main src/main.c:359
    #25 0x74114d034e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #26 0x74114d034ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #27 0x5d79ec82f3f4 in _start (/home/jeremiah/Beginners-Guide-to-SDL3-in-C/beginners-guide-sdl3-c+0x23f4) (BuildId: c890681ba21576c9acf9a6e8235532611d6582d9)

Direct leak of 96 byte(s) in 1 object(s) allocated from:
    #0 0x74114d6fd1aa in calloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x74114c38e4de  (<unknown module>)
    #2 0x74114c38f193  (<unknown module>)
    #3 0x74114c3904cb  (<unknown module>)
    #4 0x74114d379055  (/usr/lib/libSDL3.so.0+0x179055) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #5 0x74114d21d4fd  (/usr/lib/libSDL3.so.0+0x1d4fd) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #6 0x5d79ec82f566 in game_init_sdl src/main.c:58
    #7 0x5d79ec83040f in game_new src/main.c:174
    #8 0x5d79ec831994 in main src/main.c:359
    #9 0x74114d034e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #10 0x74114d034ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #11 0x5d79ec82f3f4 in _start (/home/jeremiah/Beginners-Guide-to-SDL3-in-C/beginners-guide-sdl3-c+0x23f4) (BuildId: c890681ba21576c9acf9a6e8235532611d6582d9)

Indirect leak of 144 byte(s) in 1 object(s) allocated from:
    #0 0x74114d6fd1aa in calloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x741145d368c7  (<unknown module>)
    #2 0x741145d36c53  (<unknown module>)
    #3 0x741145d3b921  (<unknown module>)
    #4 0x741145d647eb  (<unknown module>)
    #5 0x741145d59840  (<unknown module>)
    #6 0x74114d306e31  (/usr/lib/libSDL3.so.0+0x106e31) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #7 0x74114d370329  (/usr/lib/libSDL3.so.0+0x170329) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #8 0x74114d31c852  (/usr/lib/libSDL3.so.0+0x11c852) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #9 0x74114d322b2e  (/usr/lib/libSDL3.so.0+0x122b2e) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #10 0x74114d291cd1  (/usr/lib/libSDL3.so.0+0x91cd1) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #11 0x74114d2805d5  (/usr/lib/libSDL3.so.0+0x805d5) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #12 0x74114d2807d6  (/usr/lib/libSDL3.so.0+0x807d6) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #13 0x5d79ec82f8cb in game_init_sdl src/main.c:90
    #14 0x5d79ec83040f in game_new src/main.c:174
    #15 0x5d79ec831994 in main src/main.c:359
    #16 0x74114d034e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #17 0x74114d034ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #18 0x5d79ec82f3f4 in _start (/home/jeremiah/Beginners-Guide-to-SDL3-in-C/beginners-guide-sdl3-c+0x23f4) (BuildId: c890681ba21576c9acf9a6e8235532611d6582d9)

Indirect leak of 40 byte(s) in 1 object(s) allocated from:
    #0 0x74114d6fd1aa in calloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x741145d6485f  (<unknown module>)
    #2 0x741145d59840  (<unknown module>)
    #3 0x74114d306e31  (/usr/lib/libSDL3.so.0+0x106e31) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #4 0x74114d370329  (/usr/lib/libSDL3.so.0+0x170329) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #5 0x74114d31c852  (/usr/lib/libSDL3.so.0+0x11c852) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #6 0x74114d322b2e  (/usr/lib/libSDL3.so.0+0x122b2e) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #7 0x74114d291cd1  (/usr/lib/libSDL3.so.0+0x91cd1) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #8 0x74114d2805d5  (/usr/lib/libSDL3.so.0+0x805d5) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #9 0x74114d2807d6  (/usr/lib/libSDL3.so.0+0x807d6) (BuildId: 3c9f784f4962261f7624483ae4bd4029a31f8e32)
    #10 0x5d79ec82f8cb in game_init_sdl src/main.c:90
    #11 0x5d79ec83040f in game_new src/main.c:174
    #12 0x5d79ec831994 in main src/main.c:359
    #13 0x74114d034e07  (/usr/lib/libc.so.6+0x25e07) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #14 0x74114d034ecb in __libc_start_main (/usr/lib/libc.so.6+0x25ecb) (BuildId: aed3a2b0cf4e6cc12296052529af22f6a450a75a)
    #15 0x5d79ec82f3f4 in _start (/home/jeremiah/Beginners-Guide-to-SDL3-in-C/beginners-guide-sdl3-c+0x23f4) (BuildId: c890681ba21576c9acf9a6e8235532611d6582d9)

SUMMARY: AddressSanitizer: 3232 byte(s) leaked in 5 allocation(s).
```

## Comment 2627867026

maintainer (COLLABORATOR) · slouken · 2025-01-31T17:30:05Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2627867026

@ProgrammingRainbow, thank you for setting up a bunch of test cases for us to investigate. We will come back to this, but are prioritizing game breaking bugs over memory leaks at the moment.

## Comment 2627905425

maintainer (COLLABORATOR) · icculus · 2025-01-31T17:46:12Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2627905425

> This is pretty clear that we shouldn't do this by default and that SDL_SHUTDOWN_DBUS_ON_QUIT should only be set by people trying to do memory leak detection.

Ugh, okay.  :/

## Comment 2627935299

maintainer (COLLABORATOR) · icculus · 2025-01-31T17:49:52Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2627935299

For the XrmInititalize leak, I'm thinking we should try other approaches first (GDK's Xsettings key, if not the GDK_SCALE environment variable), and try Xft.dpi as a last resort, so we don't leak the memory if there was a better option. But I don't really know the ramifications of that, or which of these things are more or less reliable.

## Comment 2627977240

other (CONTRIBUTOR) · Kontrabant · 2025-01-31T17:54:37Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2627977240

Note that Wayland won't check-out perfectly clean either, particularly if the desktop requires libdecor, which loads cairo/GTK for drawing window decorations, which have some leaks of their own.

## Comment 2628006228

maintainer (COLLABORATOR) · slouken · 2025-01-31T18:07:13Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2628006228

> For the XrmInititalize leak, I'm thinking we should try other approaches first (GDK's Xsettings key, if not the GDK_SCALE environment variable), and try Xft.dpi as a last resort, so we don't leak the memory if there was a better option. But I don't really know the ramifications of that, or which of these things are more or less reliable.

Based on the discussion in https://github.com/libsdl-org/SDL/issues/11142, we are checking scale options in the correct order, and Xft.dpi should be preferred.

## Comment 2628007749

maintainer (COLLABORATOR) · slouken · 2025-01-31T18:08:09Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2628007749

In general we can't control leaks in other libraries and we shouldn't be doing gyrations to avoid them. Anyone who finds those leaks while investigating them in SDL can report them upstream.

## Comment 2628009366

other (CONTRIBUTOR) · madebr · 2025-01-31T18:09:07Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2628009366

Running `testsprite` from SDL3.
Ironically, when I disable unloading the DBUS library, then running testsprite with SDL3, built with `-fsanitize=address`, does not complain about DBUS leaks upon exit.
```patch
--- a/src/core/linux/SDL_dbus.c
+++ b/src/core/linux/SDL_dbus.c
@@ -98,7 +98,7 @@ static bool LoadDBUSSyms(void)
 static void UnloadDBUSLibrary(void)
 {
     if (dbus_handle) {
-        SDL_UnloadObject(dbus_handle);
+//        SDL_UnloadObject(dbus_handle);
         dbus_handle = NULL;
     }
 }
```

Perhaps AddressSanitizer has special rules to ignore dbus leaks?
Perhaps, we are interfering with this ignore rule?

## Comment 2628073537

reporter (NONE) · ProgrammingRainbow · 2025-01-31T18:50:00Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2628073537

All those I posted above where all in wayland with the dbus switch. 

## Comment 2635400029

other (CONTRIBUTOR) · cgutman · 2025-02-05T00:07:12Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2635400029

I think @madebr is on the right track. It's not that ASan treats D-Bus differently; it treats _any_ shared libraries that have not unloaded as exempt from leak checking. This is sensible because any loaded shared libraries could have legitimate memory allocations owned internally to the library that would be falsely detected as leaks in the application upon exit.

Because we're calling `dlclose()` on libdbus without calling `dbus_shutdown()`, ASan thinks all allocations from libdbus should be freed and warns that they are not. https://github.com/libsdl-org/SDL/pull/12190 avoids these false leak warnings by keeping the library loaded.

See also the upstream report on this behavior which also suggests leaving it loaded: https://gitlab.freedesktop.org/dbus/dbus/-/issues/495

## Comment 2636050424

maintainer (COLLABORATOR) · slouken · 2025-02-05T08:25:37Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2636050424

@ProgrammingRainbow, the memory leaks are much improved in the latest main code for sdl2-compat and SDL3.

I tested on Ubuntu 24.04 using X11 and XWayland, and these were my results:
```
~/projects/Yellow-Snow-Cpp-SDL2$ ./yellow-snow
all clean!
~/projects/Conways-Game-of-Life-C-SDL2$ ./game-of-life
all clean!
~/projects/Conways-Game-of-Life-Cpp-SDL2$ ./game-of-life
all clean!
~/projects/Minesweeper-C-SDL2$ ./minesweeper
border clean.
board clean.
mines clean.
clock clean.
face clean.
all clean!
~/projects/Minesweeper-Cpp-SDL2$ ./minesweeper
all clean!
~/projects/Beginners-Guide-to-SDL3-in-C$ ./beginners-guide-sdl3-c
all clean!
~/projects/Beginners-Guide-to-SDL3-in-Cpp$ ./beginners-guide-sdl3-cpp
```

Note that I did not set any environment variables. As @Kontrabant noted, libdecor has known memory leaks and is used for window decorations when the Wayland video driver is enabled.

What do you see?

## Comment 2636065325

maintainer (COLLABORATOR) · slouken · 2025-02-05T08:33:11Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2636065325

Just for grins I ran both SDL2 and sdl2-compat using `SDL_VIDEODRIVER=wayland` and got a ton of memory leaks outside SDL, as expected.

SDL2:
```
~/projects/Yellow-Snow-Cpp-SDL2$ SDL_VIDEODRIVER=wayland ./yellow-snow 
...
SUMMARY: AddressSanitizer: 35039 byte(s) leaked in 1175 allocation(s).
```

sdl2-compat:
```
~/projects/Yellow-Snow-Cpp-SDL2$ SDL_VIDEODRIVER=wayland ./yellow-snow 
...
SUMMARY: AddressSanitizer: 34254 byte(s) leaked in 1173 allocation(s).
```

However, when using X11 and XWayland I'm not seeing any leaks here.

It seems like SDL2 and sdl2-compat are now about the same in terms of memory leaks.

## Comment 2636099635

maintainer (COLLABORATOR) · slouken · 2025-02-05T08:50:07Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2636099635

Just for fun I wanted to see how many of the Wayland leaks were from SDL itself.

I created a file `asan-third-party.txt` with the contents:
```
leak:fontconfig
leak:libdecor
```

This will ignore any leaks from the third party libdecor and fontconfig libraries, which are known to leak.

Then I ran yellow-snow using this file:
```
~/projects/Yellow-Snow-Cpp-SDL2$ LSAN_OPTIONS="suppressions=asan-third-party.txt" SDL_VIDEODRIVER=wayland ./yellow-snow 
all clean!

=================================================================
==20278==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 2688 byte(s) in 1 object(s) allocated from:
    #0 0x767bdf4fd340 in calloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x767bd31c381e  (/usr/local/lib/libSDL2-2.0.so.0.3000.53+0xc681e)
    #2 0x767bd31c3edf  (/usr/local/lib/libSDL2-2.0.so.0.3000.53+0xc6edf)
    #3 0x767bd5d19144  (<unknown module>)
    #4 0x767bda1b8443 in SDL_EGL_LoadLibrary /home/slouken/projects/SDL/src/video/SDL_egl.c:554
    #5 0x767bda2b1e23 in Wayland_GLES_LoadLibrary /home/slouken/projects/SDL/src/video/wayland/SDL_waylandopengles.c:42
    #6 0x767bda1d7c55 in SDL_GL_LoadLibrary_REAL /home/slouken/projects/SDL/src/video/SDL_video.c:4351
    #7 0x767bda1d2ccd in SDL_RecreateWindow /home/slouken/projects/SDL/src/video/SDL_video.c:2634
    #8 0x767bda0d43d7 in GL_CreateRenderer /home/slouken/projects/SDL/src/render/opengl/SDL_render_gl.c:1631
    #9 0x767bda0b9d94 in SDL_CreateRendererWithProperties_REAL /home/slouken/projects/SDL/src/render/SDL_render.c:1034
    #10 0x767bda0ba27f in SDL_CreateRenderer_REAL /home/slouken/projects/SDL/src/render/SDL_render.c:1167
    #11 0x767bda06feed in SDL_CreateRenderer /home/slouken/projects/SDL/src/dynapi/SDL_dynapi_procs.h:148
    #12 0x767bdfbbb62e in SDL_CreateRenderer_REAL /home/slouken/projects/sdl2-compat-experimental/src/sdl2_compat.c:4605
    #13 0x767bdfbd3826 in SDL_CreateRenderer /home/slouken/projects/sdl2-compat-experimental/src/dynapi/SDL_dynapi_procs.h:328
    #14 0x5bb42ef237d6 in Game::initSdl() src/init_sdl.cpp:42
    #15 0x5bb42eeeb4f2 in Game::init() src/game.cpp:33
    #16 0x5bb42ef27d47 in main src/main.cpp:6
    #17 0x767bdea2a1c9 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #18 0x767bdea2a28a in __libc_start_main_impl ../csu/libc-start.c:360
    #19 0x5bb42eee61c4 in _start (/home/slouken/projects/Yellow-Snow-Cpp-SDL2/yellow-snow+0x181c4) (BuildId: e9f97466f215054846e5bc0c1127945df75a554e)

Indirect leak of 144 byte(s) in 1 object(s) allocated from:
    #0 0x767bdf4fd340 in calloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x767bd4725ef6  (<unknown module>)
    #2 0x767bd4726273  (<unknown module>)
    #3 0x767bd472ac98  (<unknown module>)
    #4 0x767bd31c32ac  (/usr/local/lib/libSDL2-2.0.so.0.3000.53+0xc62ac)
    #5 0x767bd31b88af  (/usr/local/lib/libSDL2-2.0.so.0.3000.53+0xbb8af)
    #6 0x767bda1b84ba in SDL_EGL_LoadLibrary /home/slouken/projects/SDL/src/video/SDL_egl.c:562
    #7 0x767bda2b1e23 in Wayland_GLES_LoadLibrary /home/slouken/projects/SDL/src/video/wayland/SDL_waylandopengles.c:42
    #8 0x767bda1d7c55 in SDL_GL_LoadLibrary_REAL /home/slouken/projects/SDL/src/video/SDL_video.c:4351
    #9 0x767bda1d2ccd in SDL_RecreateWindow /home/slouken/projects/SDL/src/video/SDL_video.c:2634
    #10 0x767bda0d43d7 in GL_CreateRenderer /home/slouken/projects/SDL/src/render/opengl/SDL_render_gl.c:1631
    #11 0x767bda0b9d94 in SDL_CreateRendererWithProperties_REAL /home/slouken/projects/SDL/src/render/SDL_render.c:1034
    #12 0x767bda0ba27f in SDL_CreateRenderer_REAL /home/slouken/projects/SDL/src/render/SDL_render.c:1167
    #13 0x767bda06feed in SDL_CreateRenderer /home/slouken/projects/SDL/src/dynapi/SDL_dynapi_procs.h:148
    #14 0x767bdfbbb62e in SDL_CreateRenderer_REAL /home/slouken/projects/sdl2-compat-experimental/src/sdl2_compat.c:4605
    #15 0x767bdfbd3826 in SDL_CreateRenderer /home/slouken/projects/sdl2-compat-experimental/src/dynapi/SDL_dynapi_procs.h:328
    #16 0x5bb42ef237d6 in Game::initSdl() src/init_sdl.cpp:42
    #17 0x5bb42eeeb4f2 in Game::init() src/game.cpp:33
    #18 0x5bb42ef27d47 in main src/main.cpp:6
    #19 0x767bdea2a1c9 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #20 0x767bdea2a28a in __libc_start_main_impl ../csu/libc-start.c:360
    #21 0x5bb42eee61c4 in _start (/home/slouken/projects/Yellow-Snow-Cpp-SDL2/yellow-snow+0x181c4) (BuildId: e9f97466f215054846e5bc0c1127945df75a554e)

Indirect leak of 40 byte(s) in 1 object(s) allocated from:
    #0 0x767bdf4fd340 in calloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x767bd31c331d  (/usr/local/lib/libSDL2-2.0.so.0.3000.53+0xc631d)
    #2 0x767bd31b88af  (/usr/local/lib/libSDL2-2.0.so.0.3000.53+0xbb8af)
    #3 0x767bda1b84ba in SDL_EGL_LoadLibrary /home/slouken/projects/SDL/src/video/SDL_egl.c:562
    #4 0x767bda2b1e23 in Wayland_GLES_LoadLibrary /home/slouken/projects/SDL/src/video/wayland/SDL_waylandopengles.c:42
    #5 0x767bda1d7c55 in SDL_GL_LoadLibrary_REAL /home/slouken/projects/SDL/src/video/SDL_video.c:4351
    #6 0x767bda1d2ccd in SDL_RecreateWindow /home/slouken/projects/SDL/src/video/SDL_video.c:2634
    #7 0x767bda0d43d7 in GL_CreateRenderer /home/slouken/projects/SDL/src/render/opengl/SDL_render_gl.c:1631
    #8 0x767bda0b9d94 in SDL_CreateRendererWithProperties_REAL /home/slouken/projects/SDL/src/render/SDL_render.c:1034
    #9 0x767bda0ba27f in SDL_CreateRenderer_REAL /home/slouken/projects/SDL/src/render/SDL_render.c:1167
    #10 0x767bda06feed in SDL_CreateRenderer /home/slouken/projects/SDL/src/dynapi/SDL_dynapi_procs.h:148
    #11 0x767bdfbbb62e in SDL_CreateRenderer_REAL /home/slouken/projects/sdl2-compat-experimental/src/sdl2_compat.c:4605
    #12 0x767bdfbd3826 in SDL_CreateRenderer /home/slouken/projects/sdl2-compat-experimental/src/dynapi/SDL_dynapi_procs.h:328
    #13 0x5bb42ef237d6 in Game::initSdl() src/init_sdl.cpp:42
    #14 0x5bb42eeeb4f2 in Game::init() src/game.cpp:33
    #15 0x5bb42ef27d47 in main src/main.cpp:6
    #16 0x767bdea2a1c9 in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #17 0x767bdea2a28a in __libc_start_main_impl ../csu/libc-start.c:360
    #18 0x5bb42eee61c4 in _start (/home/slouken/projects/Yellow-Snow-Cpp-SDL2/yellow-snow+0x181c4) (BuildId: e9f97466f215054846e5bc0c1127945df75a554e)

-----------------------------------------------------
Suppressions used:
  count      bytes template
   1169      31286 fontconfig
      1         96 libdecor
-----------------------------------------------------

SUMMARY: AddressSanitizer: 2872 byte(s) leaked in 3 allocation(s).
```

Looking at the leaks they seem to be inside the OpenGL driver on my system, and if so, they should go away if we stop unloading the OpenGL driver so asan can track the allocations.

So I applied this patch to SDL to do that:
```diff
diff --git a/src/video/SDL_egl.c b/src/video/SDL_egl.c
index 86502549b..92817f937 100644
--- a/src/video/SDL_egl.c
+++ b/src/video/SDL_egl.c
@@ -284,11 +284,11 @@ void SDL_EGL_UnloadLibrary(SDL_VideoDevice *_this)
         }
 
         if (_this->egl_data->egl_dll_handle) {
-            SDL_UnloadObject(_this->egl_data->egl_dll_handle);
+            //SDL_UnloadObject(_this->egl_data->egl_dll_handle);
             _this->egl_data->egl_dll_handle = NULL;
         }
         if (_this->egl_data->opengl_dll_handle) {
-            SDL_UnloadObject(_this->egl_data->opengl_dll_handle);
+            //SDL_UnloadObject(_this->egl_data->opengl_dll_handle);
             _this->egl_data->opengl_dll_handle = NULL;
         }
 
```

Now the result looks much nicer:
```
~/projects/Yellow-Snow-Cpp-SDL2$ LSAN_OPTIONS="suppressions=asan-third-party.txt" SDL_VIDEODRIVER=wayland ./yellow-snow 
all clean!
-----------------------------------------------------
Suppressions used:
  count      bytes template
   1169      31286 fontconfig
      1         96 libdecor
-----------------------------------------------------
```

So SDL itself seems to be in a pretty good place, even when using the Wayland driver.

Cheers!

## Comment 2638025874

maintainer (COLLABORATOR) · icculus · 2025-02-05T21:08:27Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2638025874

It looks like Sam made good progress here, but how do we deal with the leaks out of our control?

I'd like to find a solution, both so they don't bother ProgrammingRainbow in daily use, but also so we don't get bug reports caused by other libraries as time goes on.

Do we want to generalize the dbus_shutdown hint to something like SDL_HINT_ADDRESS_SANITIZER (or detect AddressSanitizer at runtime...?) and not dlclose misbehaving libraries in those cases?

It seems wild to avoid leak reports by _leaking library handles_, and I also want to know when we've caused a legitimate leak in memory allocated on our behalf by the library that we failed to free, so a blanket disabling like this is undesirable. 

Maybe we add a FAQ that says "use this suppression file" and supply something that picks out the things like the neverFreeTable in Xlib, libdecor's leaks, etc., and not the whole library.

But automating this somehow would be nicer...I'll read up on AddressSanitizer best practices when I get a moment.

## Comment 2643075617

reporter (NONE) · ProgrammingRainbow · 2025-02-07T14:24:29Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2643075617

 I have changed this post from the original because i was in C++ at the time using smart pointers and wanted to double check i wasn't mistaken. So the original has been removed and this put in it's place. However all i am changing is the code.

Original:
@slouken Yeah it builds and runs clean now. Now i wonder if the problem has been fixed or hidden? For fun lets check. What if we just didn't free any of the memory allocated at all. Would that build and run cleanly too?

New:
```
void game_free(struct Game **game) {
    if (*game) {
        struct Game *g = *game;

        Mix_HaltMusic();
        Mix_HaltChannel(-1);

        player_free(&g->player);
        flakes_free(&g->flakes);
        score_free(&g->score);
        fps_free(&g->fps);

        if (g->hit_sound) {
            Mix_FreeChunk(g->hit_sound);
            g->hit_sound = NULL;
        }

        if (g->collect_sound) {
            Mix_FreeChunk(g->collect_sound);
            g->collect_sound = NULL;
        }

        if (g->winter_music) {
            Mix_FreeMusic(g->winter_music);
            g->winter_music = NULL;
        }

        /*if (g->white_image) {*/
        /*    SDL_DestroyTexture(g->white_image);*/
        /*    g->white_image = NULL;*/
        /*}*/

        /*if (g->yellow_image) {*/
        /*    SDL_DestroyTexture(g->yellow_image);*/
        /*    g->yellow_image = NULL;*/
        /*}*/

        /*if (g->player_image) {*/
        /*    SDL_DestroyTexture(g->player_image);*/
        /*    g->player_image = NULL;*/
        /*}*/

        /*if (g->background_image) {*/
        /*    SDL_DestroyTexture(g->background_image);*/
        /*    g->background_image = NULL;*/
        /*}*/

        /*if (g->renderer) {*/
        /*    SDL_DestroyRenderer(g->renderer);*/
        /*    g->renderer = NULL;*/
        /*}*/

        /*if (g->window) {*/
        /*    SDL_DestroyWindow(g->window);*/
        /*    g->window = NULL;*/
        /*}*/

        /*Mix_CloseAudio();*/
        /*TTF_Quit();*/
        /*Mix_Quit();*/
        /*SDL_Quit();*/

        free(g);
        g = NULL;
        *game = NULL;
    }
}
```

Original:
And amazingly it does. No issues at all. We no longer need to free memory in C hurray! But it doesn't seem to extend to all C just some parts that don't seem to be documented which.

    float *mytest = (float *)calloc(500, sizeof(float));
    (void)mytest;

This still gets flagged. So i guess i can't trust any of my SDL2 code now. Since it could be hallucinating like the ai now.

New:
All of the memory allocated by SDL2 doesn't report leaks now even when not freed. However the SDL2_mixer memory still does.



## Comment 2643688238

maintainer (COLLABORATOR) · icculus · 2025-02-07T18:26:01Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2643688238

We definitely don't want to _hide_ app leaks, or leaks in SDL itself.

I'll try to reproduce it today.

## Comment 2643700619

maintainer (COLLABORATOR) · slouken · 2025-02-07T18:33:36Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2643700619

I'm able to reproduce this. SDL_Quit() isn't called, but no leaks are reported. Oddly, if I add an intentional leak in SDL.c, that gets reported properly.

## Comment 2643727286

maintainer (COLLABORATOR) · icculus · 2025-02-07T18:50:12Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2643727286

Also, reading up on suppressions:

https://github.com/google/sanitizers/wiki/AddressSanitizerLeakSanitizer#suppressions


I'm thinking we should _not_ do things like refuse to dlclose libraries, etc, but rather provide a suppression file and a FAQ on how to use it. This will limit the leaks we "hide" to known leaks in system libraries, but also allow us to still see legit leaks we caused in those libraries (like if we fail to destroy an X11 window or whatever). Added benefit, we don't need to do things like attempt to detect AddressSanitizer or make code changes to pacify it: we just say "set this environment variable to the path of this text file."

To be clear, this is separate from today's problem where we seem to be hiding legitimate leaks.

## Comment 2644136041

other (CONTRIBUTOR) · Sackzement · 2025-02-07T21:11:23Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2644136041

On the dbus leaks.

Using SDL2 version 2.30.12 and then just calling `SDL_Init()` and `SDL_Quit()` also reports leaks.
But surprisingly,  when using SDL3, there are no leaks.

~~How come SDL3 doesn't leak but sdl2-compat does?~~
Nevermind, seems to be fixed in sdl2-compat 2.30.54.



```c
#include <SDL2/SDL.h>

int main(void) {
    if (SDL_Init(0)) {
        SDL_Log("Error: SDL_Init(0) : %s\n", SDL_GetError());
        return -1;
    }
    
    SDL_Quit();
    
    return 0;
}

```

<details><summary>Output</summary>
<p>

```shell

=================================================================
==1065922==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 520 byte(s) in 13 object(s) allocated from:
    #0 0x7b4fda6fd721 in malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x7b4fdad185ea  (<unknown module>)
    #2 0x7b4fdad0d094  (<unknown module>)
    #3 0x7b4fda42201a in SDL_DBus_Init_Spinlocked /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:145
    #4 0x7b4fda42212f in SDL_DBus_Init /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:175
    #5 0x7b4fda22825d in SDL_InitSubSystem_REAL /path/to/SDL-2.30.12/src/SDL.c:225
    #6 0x7b4fda2284a7 in SDL_Init_REAL /path/to/SDL-2.30.12/src/SDL.c:394
    #7 0x7b4fda244070 in SDL_Init_DEFAULT /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #8 0x7b4fda24d055 in SDL_Init /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #9 0x5fe9bf8a91b6 in main /path/to/SDL-bugtest/src/main.c:4
    #10 0x7b4fda035487  (/usr/lib/libc.so.6+0x27487) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #11 0x7b4fda03554b in __libc_start_main (/usr/lib/libc.so.6+0x2754b) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #12 0x5fe9bf8a90d4 in _start (/path/to/SDL-bugtest/build/SDL-bugtest+0x10d4) (BuildId: a68b569832c001aa6cc12658ee1341c78728de1f)

Direct leak of 368 byte(s) in 2 object(s) allocated from:
    #0 0x7b4fda6fd02a in calloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x7b4fdad06ac3  (<unknown module>)
    #2 0x7b4fdad08bbd  (<unknown module>)
    #3 0x7b4fdad138ce  (<unknown module>)
    #4 0x7b4fdad13ac7  (<unknown module>)
    #5 0x7b4fdad13e20  (<unknown module>)
    #6 0x7b4fdad143ac  (<unknown module>)
    #7 0x7b4fdacf7e82  (/usr/lib/libasan.so.8.0.0+0xa4ce82)
    #8 0x7b4fdad0cb9f  (<unknown module>)
    #9 0x7b4fdacf9d36  (/usr/lib/libasan.so.8.0.0+0xa4ed36)
    #10 0x7b4fdacf9fdd  (/usr/lib/libasan.so.8.0.0+0xa4efdd)
    #11 0x7b4fdacfa2ca  (/usr/lib/libasan.so.8.0.0+0xa4f2ca)
    #12 0x7b4fda4220bb in SDL_DBus_Init_Spinlocked /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:163
    #13 0x7b4fda42212f in SDL_DBus_Init /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:175
    #14 0x7b4fda22825d in SDL_InitSubSystem_REAL /path/to/SDL-2.30.12/src/SDL.c:225
    #15 0x7b4fda2284a7 in SDL_Init_REAL /path/to/SDL-2.30.12/src/SDL.c:394
    #16 0x7b4fda244070 in SDL_Init_DEFAULT /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #17 0x7b4fda24d055 in SDL_Init /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #18 0x5fe9bf8a91b6 in main /path/to/SDL-bugtest/src/main.c:4
    #19 0x7b4fda035487  (/usr/lib/libc.so.6+0x27487) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #20 0x7b4fda03554b in __libc_start_main (/usr/lib/libc.so.6+0x2754b) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #21 0x5fe9bf8a90d4 in _start (/path/to/SDL-bugtest/build/SDL-bugtest+0x10d4) (BuildId: a68b569832c001aa6cc12658ee1341c78728de1f)

Direct leak of 184 byte(s) in 1 object(s) allocated from:
    #0 0x7b4fda6fd02a in calloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x7b4fdad06ac3  (<unknown module>)
    #2 0x7b4fdad07948  (<unknown module>)
    #3 0x7b4fdacf9fbd  (/usr/lib/libasan.so.8.0.0+0xa4efbd)
    #4 0x7b4fdacfa2ca  (/usr/lib/libasan.so.8.0.0+0xa4f2ca)
    #5 0x7b4fda422052 in SDL_DBus_Init_Spinlocked /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:153
    #6 0x7b4fda42212f in SDL_DBus_Init /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:175
    #7 0x7b4fda22825d in SDL_InitSubSystem_REAL /path/to/SDL-2.30.12/src/SDL.c:225
    #8 0x7b4fda2284a7 in SDL_Init_REAL /path/to/SDL-2.30.12/src/SDL.c:394
    #9 0x7b4fda244070 in SDL_Init_DEFAULT /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #10 0x7b4fda24d055 in SDL_Init /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #11 0x5fe9bf8a91b6 in main /path/to/SDL-bugtest/src/main.c:4
    #12 0x7b4fda035487  (/usr/lib/libc.so.6+0x27487) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #13 0x7b4fda03554b in __libc_start_main (/usr/lib/libc.so.6+0x2754b) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #14 0x5fe9bf8a90d4 in _start (/path/to/SDL-bugtest/build/SDL-bugtest+0x10d4) (BuildId: a68b569832c001aa6cc12658ee1341c78728de1f)

Direct leak of 184 byte(s) in 1 object(s) allocated from:
    #0 0x7b4fda6fd02a in calloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x7b4fdad06ac3  (<unknown module>)
    #2 0x7b4fdad07e56  (<unknown module>)
    #3 0x7b4fdacf9930  (/usr/lib/libasan.so.8.0.0+0xa4e930)
    #4 0x7b4fdacf9d1b  (/usr/lib/libasan.so.8.0.0+0xa4ed1b)
    #5 0x7b4fdacf9fdd  (/usr/lib/libasan.so.8.0.0+0xa4efdd)
    #6 0x7b4fdacfa2ca  (/usr/lib/libasan.so.8.0.0+0xa4f2ca)
    #7 0x7b4fda422052 in SDL_DBus_Init_Spinlocked /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:153
    #8 0x7b4fda42212f in SDL_DBus_Init /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:175
    #9 0x7b4fda22825d in SDL_InitSubSystem_REAL /path/to/SDL-2.30.12/src/SDL.c:225
    #10 0x7b4fda2284a7 in SDL_Init_REAL /path/to/SDL-2.30.12/src/SDL.c:394
    #11 0x7b4fda244070 in SDL_Init_DEFAULT /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #12 0x7b4fda24d055 in SDL_Init /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #13 0x5fe9bf8a91b6 in main /path/to/SDL-bugtest/src/main.c:4
    #14 0x7b4fda035487  (/usr/lib/libc.so.6+0x27487) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #15 0x7b4fda03554b in __libc_start_main (/usr/lib/libc.so.6+0x2754b) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #16 0x5fe9bf8a90d4 in _start (/path/to/SDL-bugtest/build/SDL-bugtest+0x10d4) (BuildId: a68b569832c001aa6cc12658ee1341c78728de1f)

Direct leak of 184 byte(s) in 1 object(s) allocated from:
    #0 0x7b4fda6fd02a in calloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:77
    #1 0x7b4fdad06ac3  (<unknown module>)
    #2 0x7b4fdad08bbd  (<unknown module>)
    #3 0x7b4fdad138ce  (<unknown module>)
    #4 0x7b4fdad13ac7  (<unknown module>)
    #5 0x7b4fdad13e20  (<unknown module>)
    #6 0x7b4fdad143ac  (<unknown module>)
    #7 0x7b4fdacf7e82  (/usr/lib/libasan.so.8.0.0+0xa4ce82)
    #8 0x7b4fdad0cb9f  (<unknown module>)
    #9 0x7b4fdacf9d36  (/usr/lib/libasan.so.8.0.0+0xa4ed36)
    #10 0x7b4fdacf9fdd  (/usr/lib/libasan.so.8.0.0+0xa4efdd)
    #11 0x7b4fdacfa2ca  (/usr/lib/libasan.so.8.0.0+0xa4f2ca)
    #12 0x7b4fda422052 in SDL_DBus_Init_Spinlocked /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:153
    #13 0x7b4fda42212f in SDL_DBus_Init /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:175
    #14 0x7b4fda22825d in SDL_InitSubSystem_REAL /path/to/SDL-2.30.12/src/SDL.c:225
    #15 0x7b4fda2284a7 in SDL_Init_REAL /path/to/SDL-2.30.12/src/SDL.c:394
    #16 0x7b4fda244070 in SDL_Init_DEFAULT /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #17 0x7b4fda24d055 in SDL_Init /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #18 0x5fe9bf8a91b6 in main /path/to/SDL-bugtest/src/main.c:4
    #19 0x7b4fda035487  (/usr/lib/libc.so.6+0x27487) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #20 0x7b4fda03554b in __libc_start_main (/usr/lib/libc.so.6+0x2754b) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #21 0x5fe9bf8a90d4 in _start (/path/to/SDL-bugtest/build/SDL-bugtest+0x10d4) (BuildId: a68b569832c001aa6cc12658ee1341c78728de1f)

Direct leak of 38 byte(s) in 1 object(s) allocated from:
    #0 0x7b4fda6fd721 in malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x7b4fdad15345  (<unknown module>)
    #2 0x7b4fdacfa4b2  (/usr/lib/libasan.so.8.0.0+0xa4f4b2)
    #3 0x7b4fda422052 in SDL_DBus_Init_Spinlocked /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:153
    #4 0x7b4fda42212f in SDL_DBus_Init /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:175
    #5 0x7b4fda22825d in SDL_InitSubSystem_REAL /path/to/SDL-2.30.12/src/SDL.c:225
    #6 0x7b4fda2284a7 in SDL_Init_REAL /path/to/SDL-2.30.12/src/SDL.c:394
    #7 0x7b4fda244070 in SDL_Init_DEFAULT /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #8 0x7b4fda24d055 in SDL_Init /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #9 0x5fe9bf8a91b6 in main /path/to/SDL-bugtest/src/main.c:4
    #10 0x7b4fda035487  (/usr/lib/libc.so.6+0x27487) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #11 0x7b4fda03554b in __libc_start_main (/usr/lib/libc.so.6+0x2754b) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #12 0x5fe9bf8a90d4 in _start (/path/to/SDL-bugtest/build/SDL-bugtest+0x10d4) (BuildId: a68b569832c001aa6cc12658ee1341c78728de1f)

Direct leak of 29 byte(s) in 1 object(s) allocated from:
    #0 0x7b4fda6fd721 in malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x7b4fdad15345  (<unknown module>)
    #2 0x7b4fdacfa67b  (/usr/lib/libasan.so.8.0.0+0xa4f67b)
    #3 0x7b4fda422052 in SDL_DBus_Init_Spinlocked /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:153
    #4 0x7b4fda42212f in SDL_DBus_Init /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:175
    #5 0x7b4fda22825d in SDL_InitSubSystem_REAL /path/to/SDL-2.30.12/src/SDL.c:225
    #6 0x7b4fda2284a7 in SDL_Init_REAL /path/to/SDL-2.30.12/src/SDL.c:394
    #7 0x7b4fda244070 in SDL_Init_DEFAULT /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #8 0x7b4fda24d055 in SDL_Init /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #9 0x5fe9bf8a91b6 in main /path/to/SDL-bugtest/src/main.c:4
    #10 0x7b4fda035487  (/usr/lib/libc.so.6+0x27487) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #11 0x7b4fda03554b in __libc_start_main (/usr/lib/libc.so.6+0x2754b) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #12 0x5fe9bf8a90d4 in _start (/path/to/SDL-bugtest/build/SDL-bugtest+0x10d4) (BuildId: a68b569832c001aa6cc12658ee1341c78728de1f)

Direct leak of 29 byte(s) in 1 object(s) allocated from:
    #0 0x7b4fda6fd721 in malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x7b4fdad15345  (<unknown module>)
    #2 0x7b4fdacfa6c8  (/usr/lib/libasan.so.8.0.0+0xa4f6c8)
    #3 0x7b4fda422052 in SDL_DBus_Init_Spinlocked /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:153
    #4 0x7b4fda42212f in SDL_DBus_Init /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:175
    #5 0x7b4fda22825d in SDL_InitSubSystem_REAL /path/to/SDL-2.30.12/src/SDL.c:225
    #6 0x7b4fda2284a7 in SDL_Init_REAL /path/to/SDL-2.30.12/src/SDL.c:394
    #7 0x7b4fda244070 in SDL_Init_DEFAULT /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #8 0x7b4fda24d055 in SDL_Init /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #9 0x5fe9bf8a91b6 in main /path/to/SDL-bugtest/src/main.c:4
    #10 0x7b4fda035487  (/usr/lib/libc.so.6+0x27487) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #11 0x7b4fda03554b in __libc_start_main (/usr/lib/libc.so.6+0x2754b) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #12 0x5fe9bf8a90d4 in _start (/path/to/SDL-bugtest/build/SDL-bugtest+0x10d4) (BuildId: a68b569832c001aa6cc12658ee1341c78728de1f)

Direct leak of 24 byte(s) in 1 object(s) allocated from:
    #0 0x7b4fda6fd721 in malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x7b4fdad1d498  (<unknown module>)
    #2 0x7b4fdad07796  (<unknown module>)
    #3 0x7b4fdad0bb31  (<unknown module>)
    #4 0x7b4fdacf9d4d  (/usr/lib/libasan.so.8.0.0+0xa4ed4d)
    #5 0x7b4fdacf9fdd  (/usr/lib/libasan.so.8.0.0+0xa4efdd)
    #6 0x7b4fdacfa2ca  (/usr/lib/libasan.so.8.0.0+0xa4f2ca)
    #7 0x7b4fda422052 in SDL_DBus_Init_Spinlocked /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:153
    #8 0x7b4fda42212f in SDL_DBus_Init /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:175
    #9 0x7b4fda22825d in SDL_InitSubSystem_REAL /path/to/SDL-2.30.12/src/SDL.c:225
    #10 0x7b4fda2284a7 in SDL_Init_REAL /path/to/SDL-2.30.12/src/SDL.c:394
    #11 0x7b4fda244070 in SDL_Init_DEFAULT /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #12 0x7b4fda24d055 in SDL_Init /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #13 0x5fe9bf8a91b6 in main /path/to/SDL-bugtest/src/main.c:4
    #14 0x7b4fda035487  (/usr/lib/libc.so.6+0x27487) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #15 0x7b4fda03554b in __libc_start_main (/usr/lib/libc.so.6+0x2754b) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #16 0x5fe9bf8a90d4 in _start (/path/to/SDL-bugtest/build/SDL-bugtest+0x10d4) (BuildId: a68b569832c001aa6cc12658ee1341c78728de1f)

Indirect leak of 256 byte(s) in 2 object(s) allocated from:
    #0 0x7b4fda6fc3c2 in realloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:85
    #1 0x7b4fdad155a6  (<unknown module>)
    #2 0x7b4fdad15634  (<unknown module>)
    #3 0x7b4fdad1721b  (<unknown module>)
    #4 0x7b4fdad08bfd  (<unknown module>)
    #5 0x7b4fdad138ce  (<unknown module>)
    #6 0x7b4fdad13ac7  (<unknown module>)
    #7 0x7b4fdad13e20  (<unknown module>)
    #8 0x7b4fdad143ac  (<unknown module>)
    #9 0x7b4fdacf7e82  (/usr/lib/libasan.so.8.0.0+0xa4ce82)
    #10 0x7b4fdad0cb9f  (<unknown module>)
    #11 0x7b4fdacf9d36  (/usr/lib/libasan.so.8.0.0+0xa4ed36)
    #12 0x7b4fdacf9fdd  (/usr/lib/libasan.so.8.0.0+0xa4efdd)
    #13 0x7b4fdacfa2ca  (/usr/lib/libasan.so.8.0.0+0xa4f2ca)
    #14 0x7b4fda4220bb in SDL_DBus_Init_Spinlocked /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:163
    #15 0x7b4fda42212f in SDL_DBus_Init /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:175
    #16 0x7b4fda22825d in SDL_InitSubSystem_REAL /path/to/SDL-2.30.12/src/SDL.c:225
    #17 0x7b4fda2284a7 in SDL_Init_REAL /path/to/SDL-2.30.12/src/SDL.c:394
    #18 0x7b4fda244070 in SDL_Init_DEFAULT /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #19 0x7b4fda24d055 in SDL_Init /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #20 0x5fe9bf8a91b6 in main /path/to/SDL-bugtest/src/main.c:4
    #21 0x7b4fda035487  (/usr/lib/libc.so.6+0x27487) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #22 0x7b4fda03554b in __libc_start_main (/usr/lib/libc.so.6+0x2754b) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #23 0x5fe9bf8a90d4 in _start (/path/to/SDL-bugtest/build/SDL-bugtest+0x10d4) (BuildId: a68b569832c001aa6cc12658ee1341c78728de1f)

Indirect leak of 223 byte(s) in 1 object(s) allocated from:
    #0 0x7b4fda6fc3c2 in realloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:85
    #1 0x7b4fdad155a6  (<unknown module>)
    #2 0x7b4fdad15634  (<unknown module>)
    #3 0x7b4fdad1721b  (<unknown module>)
    #4 0x7b4fdad19bdc  (<unknown module>)
    #5 0x7b4fdad02ab4  (/usr/lib/libasan.so.8.0.0+0xa57ab4)
    #6 0x7b4fdad072e2  (<unknown module>)
    #7 0x7b4fdad07edc  (<unknown module>)
    #8 0x7b4fdacf9930  (/usr/lib/libasan.so.8.0.0+0xa4e930)
    #9 0x7b4fdacf9d1b  (/usr/lib/libasan.so.8.0.0+0xa4ed1b)
    #10 0x7b4fdacf9fdd  (/usr/lib/libasan.so.8.0.0+0xa4efdd)
    #11 0x7b4fdacfa2ca  (/usr/lib/libasan.so.8.0.0+0xa4f2ca)
    #12 0x7b4fda4220bb in SDL_DBus_Init_Spinlocked /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:163
    #13 0x7b4fda42212f in SDL_DBus_Init /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:175
    #14 0x7b4fda22825d in SDL_InitSubSystem_REAL /path/to/SDL-2.30.12/src/SDL.c:225
    #15 0x7b4fda2284a7 in SDL_Init_REAL /path/to/SDL-2.30.12/src/SDL.c:394
    #16 0x7b4fda244070 in SDL_Init_DEFAULT /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #17 0x7b4fda24d055 in SDL_Init /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #18 0x5fe9bf8a91b6 in main /path/to/SDL-bugtest/src/main.c:4
    #19 0x7b4fda035487  (/usr/lib/libc.so.6+0x27487) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #20 0x7b4fda03554b in __libc_start_main (/usr/lib/libc.so.6+0x2754b) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #21 0x5fe9bf8a90d4 in _start (/path/to/SDL-bugtest/build/SDL-bugtest+0x10d4) (BuildId: a68b569832c001aa6cc12658ee1341c78728de1f)

Indirect leak of 223 byte(s) in 1 object(s) allocated from:
    #0 0x7b4fda6fc3c2 in realloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:85
    #1 0x7b4fdad155a6  (<unknown module>)
    #2 0x7b4fdad15634  (<unknown module>)
    #3 0x7b4fdad1721b  (<unknown module>)
    #4 0x7b4fdad19bdc  (<unknown module>)
    #5 0x7b4fdad02ab4  (/usr/lib/libasan.so.8.0.0+0xa57ab4)
    #6 0x7b4fdad072e2  (<unknown module>)
    #7 0x7b4fdad07edc  (<unknown module>)
    #8 0x7b4fdacf9930  (/usr/lib/libasan.so.8.0.0+0xa4e930)
    #9 0x7b4fdacf9d1b  (/usr/lib/libasan.so.8.0.0+0xa4ed1b)
    #10 0x7b4fdacf9fdd  (/usr/lib/libasan.so.8.0.0+0xa4efdd)
    #11 0x7b4fdacfa2ca  (/usr/lib/libasan.so.8.0.0+0xa4f2ca)
    #12 0x7b4fda422052 in SDL_DBus_Init_Spinlocked /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:153
    #13 0x7b4fda42212f in SDL_DBus_Init /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:175
    #14 0x7b4fda22825d in SDL_InitSubSystem_REAL /path/to/SDL-2.30.12/src/SDL.c:225
    #15 0x7b4fda2284a7 in SDL_Init_REAL /path/to/SDL-2.30.12/src/SDL.c:394
    #16 0x7b4fda244070 in SDL_Init_DEFAULT /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #17 0x7b4fda24d055 in SDL_Init /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #18 0x5fe9bf8a91b6 in main /path/to/SDL-bugtest/src/main.c:4
    #19 0x7b4fda035487  (/usr/lib/libc.so.6+0x27487) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #20 0x7b4fda03554b in __libc_start_main (/usr/lib/libc.so.6+0x2754b) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #21 0x5fe9bf8a90d4 in _start (/path/to/SDL-bugtest/build/SDL-bugtest+0x10d4) (BuildId: a68b569832c001aa6cc12658ee1341c78728de1f)

Indirect leak of 176 byte(s) in 1 object(s) allocated from:
    #0 0x7b4fda6fc3c2 in realloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:85
    #1 0x7b4fdad1686d  (<unknown module>)
    #2 0x7b4fdad023e4  (/usr/lib/libasan.so.8.0.0+0xa573e4)
    #3 0x7b4fdad028bf  (/usr/lib/libasan.so.8.0.0+0xa578bf)
    #4 0x7b4fdad02cad  (/usr/lib/libasan.so.8.0.0+0xa57cad)
    #5 0x7b4fdad031b6  (/usr/lib/libasan.so.8.0.0+0xa581b6)
    #6 0x7b4fdad03248  (/usr/lib/libasan.so.8.0.0+0xa58248)
    #7 0x7b4fdad07ead  (<unknown module>)
    #8 0x7b4fdacf9930  (/usr/lib/libasan.so.8.0.0+0xa4e930)
    #9 0x7b4fdacf9d1b  (/usr/lib/libasan.so.8.0.0+0xa4ed1b)
    #10 0x7b4fdacf9fdd  (/usr/lib/libasan.so.8.0.0+0xa4efdd)
    #11 0x7b4fdacfa2ca  (/usr/lib/libasan.so.8.0.0+0xa4f2ca)
    #12 0x7b4fda4220bb in SDL_DBus_Init_Spinlocked /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:163
    #13 0x7b4fda42212f in SDL_DBus_Init /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:175
    #14 0x7b4fda22825d in SDL_InitSubSystem_REAL /path/to/SDL-2.30.12/src/SDL.c:225
    #15 0x7b4fda2284a7 in SDL_Init_REAL /path/to/SDL-2.30.12/src/SDL.c:394
    #16 0x7b4fda244070 in SDL_Init_DEFAULT /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #17 0x7b4fda24d055 in SDL_Init /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #18 0x5fe9bf8a91b6 in main /path/to/SDL-bugtest/src/main.c:4
    #19 0x7b4fda035487  (/usr/lib/libc.so.6+0x27487) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #20 0x7b4fda03554b in __libc_start_main (/usr/lib/libc.so.6+0x2754b) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #21 0x5fe9bf8a90d4 in _start (/path/to/SDL-bugtest/build/SDL-bugtest+0x10d4) (BuildId: a68b569832c001aa6cc12658ee1341c78728de1f)

Indirect leak of 160 byte(s) in 1 object(s) allocated from:
    #0 0x7b4fda6fc3c2 in realloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:85
    #1 0x7b4fdad1686d  (<unknown module>)
    #2 0x7b4fdad1ac2f  (<unknown module>)
    #3 0x7b4fdad028bf  (/usr/lib/libasan.so.8.0.0+0xa578bf)
    #4 0x7b4fdad02bf8  (/usr/lib/libasan.so.8.0.0+0xa57bf8)
    #5 0x7b4fdad031b6  (/usr/lib/libasan.so.8.0.0+0xa581b6)
    #6 0x7b4fdad03248  (/usr/lib/libasan.so.8.0.0+0xa58248)
    #7 0x7b4fdad07ead  (<unknown module>)
    #8 0x7b4fdacf9930  (/usr/lib/libasan.so.8.0.0+0xa4e930)
    #9 0x7b4fdacf9d1b  (/usr/lib/libasan.so.8.0.0+0xa4ed1b)
    #10 0x7b4fdacf9fdd  (/usr/lib/libasan.so.8.0.0+0xa4efdd)
    #11 0x7b4fdacfa2ca  (/usr/lib/libasan.so.8.0.0+0xa4f2ca)
    #12 0x7b4fda422052 in SDL_DBus_Init_Spinlocked /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:153
    #13 0x7b4fda42212f in SDL_DBus_Init /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:175
    #14 0x7b4fda22825d in SDL_InitSubSystem_REAL /path/to/SDL-2.30.12/src/SDL.c:225
    #15 0x7b4fda2284a7 in SDL_Init_REAL /path/to/SDL-2.30.12/src/SDL.c:394
    #16 0x7b4fda244070 in SDL_Init_DEFAULT /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #17 0x7b4fda24d055 in SDL_Init /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #18 0x5fe9bf8a91b6 in main /path/to/SDL-bugtest/src/main.c:4
    #19 0x7b4fda035487  (/usr/lib/libc.so.6+0x27487) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #20 0x7b4fda03554b in __libc_start_main (/usr/lib/libc.so.6+0x2754b) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #21 0x5fe9bf8a90d4 in _start (/path/to/SDL-bugtest/build/SDL-bugtest+0x10d4) (BuildId: a68b569832c001aa6cc12658ee1341c78728de1f)

Indirect leak of 160 byte(s) in 1 object(s) allocated from:
    #0 0x7b4fda6fc3c2 in realloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:85
    #1 0x7b4fdad155a6  (<unknown module>)
    #2 0x7b4fdad15634  (<unknown module>)
    #3 0x7b4fdad1721b  (<unknown module>)
    #4 0x7b4fdad19bdc  (<unknown module>)
    #5 0x7b4fdad02ab4  (/usr/lib/libasan.so.8.0.0+0xa57ab4)
    #6 0x7b4fdad02ccb  (/usr/lib/libasan.so.8.0.0+0xa57ccb)
    #7 0x7b4fdad1f2cf  (<unknown module>)
    #8 0x7b4fdad07970  (<unknown module>)
    #9 0x7b4fdacf9fbd  (/usr/lib/libasan.so.8.0.0+0xa4efbd)
    #10 0x7b4fdacfa2ca  (/usr/lib/libasan.so.8.0.0+0xa4f2ca)
    #11 0x7b4fda422052 in SDL_DBus_Init_Spinlocked /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:153
    #12 0x7b4fda42212f in SDL_DBus_Init /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:175
    #13 0x7b4fda22825d in SDL_InitSubSystem_REAL /path/to/SDL-2.30.12/src/SDL.c:225
    #14 0x7b4fda2284a7 in SDL_Init_REAL /path/to/SDL-2.30.12/src/SDL.c:394
    #15 0x7b4fda244070 in SDL_Init_DEFAULT /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #16 0x7b4fda24d055 in SDL_Init /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #17 0x5fe9bf8a91b6 in main /path/to/SDL-bugtest/src/main.c:4
    #18 0x7b4fda035487  (/usr/lib/libc.so.6+0x27487) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #19 0x7b4fda03554b in __libc_start_main (/usr/lib/libc.so.6+0x2754b) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #20 0x5fe9bf8a90d4 in _start (/path/to/SDL-bugtest/build/SDL-bugtest+0x10d4) (BuildId: a68b569832c001aa6cc12658ee1341c78728de1f)

Indirect leak of 80 byte(s) in 2 object(s) allocated from:
    #0 0x7b4fda6fd721 in malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x7b4fdad1637a  (<unknown module>)
    #2 0x7b4fdad06c56  (<unknown module>)
    #3 0x7b4fdad08bbd  (<unknown module>)
    #4 0x7b4fdad138ce  (<unknown module>)
    #5 0x7b4fdad13ac7  (<unknown module>)
    #6 0x7b4fdad13e20  (<unknown module>)
    #7 0x7b4fdad143ac  (<unknown module>)
    #8 0x7b4fdacf7e82  (/usr/lib/libasan.so.8.0.0+0xa4ce82)
    #9 0x7b4fdad0cb9f  (<unknown module>)
    #10 0x7b4fdacf9d36  (/usr/lib/libasan.so.8.0.0+0xa4ed36)
    #11 0x7b4fdacf9fdd  (/usr/lib/libasan.so.8.0.0+0xa4efdd)
    #12 0x7b4fdacfa2ca  (/usr/lib/libasan.so.8.0.0+0xa4f2ca)
    #13 0x7b4fda4220bb in SDL_DBus_Init_Spinlocked /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:163
    #14 0x7b4fda42212f in SDL_DBus_Init /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:175
    #15 0x7b4fda22825d in SDL_InitSubSystem_REAL /path/to/SDL-2.30.12/src/SDL.c:225
    #16 0x7b4fda2284a7 in SDL_Init_REAL /path/to/SDL-2.30.12/src/SDL.c:394
    #17 0x7b4fda244070 in SDL_Init_DEFAULT /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #18 0x7b4fda24d055 in SDL_Init /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #19 0x5fe9bf8a91b6 in main /path/to/SDL-bugtest/src/main.c:4
    #20 0x7b4fda035487  (/usr/lib/libc.so.6+0x27487) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #21 0x7b4fda03554b in __libc_start_main (/usr/lib/libc.so.6+0x2754b) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #22 0x5fe9bf8a90d4 in _start (/path/to/SDL-bugtest/build/SDL-bugtest+0x10d4) (BuildId: a68b569832c001aa6cc12658ee1341c78728de1f)

Indirect leak of 40 byte(s) in 1 object(s) allocated from:
    #0 0x7b4fda6fd721 in malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x7b4fdad1637a  (<unknown module>)
    #2 0x7b4fdad06c56  (<unknown module>)
    #3 0x7b4fdad07948  (<unknown module>)
    #4 0x7b4fdacf9fbd  (/usr/lib/libasan.so.8.0.0+0xa4efbd)
    #5 0x7b4fdacfa2ca  (/usr/lib/libasan.so.8.0.0+0xa4f2ca)
    #6 0x7b4fda422052 in SDL_DBus_Init_Spinlocked /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:153
    #7 0x7b4fda42212f in SDL_DBus_Init /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:175
    #8 0x7b4fda22825d in SDL_InitSubSystem_REAL /path/to/SDL-2.30.12/src/SDL.c:225
    #9 0x7b4fda2284a7 in SDL_Init_REAL /path/to/SDL-2.30.12/src/SDL.c:394
    #10 0x7b4fda244070 in SDL_Init_DEFAULT /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #11 0x7b4fda24d055 in SDL_Init /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #12 0x5fe9bf8a91b6 in main /path/to/SDL-bugtest/src/main.c:4
    #13 0x7b4fda035487  (/usr/lib/libc.so.6+0x27487) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #14 0x7b4fda03554b in __libc_start_main (/usr/lib/libc.so.6+0x2754b) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #15 0x5fe9bf8a90d4 in _start (/path/to/SDL-bugtest/build/SDL-bugtest+0x10d4) (BuildId: a68b569832c001aa6cc12658ee1341c78728de1f)

Indirect leak of 24 byte(s) in 1 object(s) allocated from:
    #0 0x7b4fda6fd721 in malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x7b4fdad1d498  (<unknown module>)
    #2 0x7b4fdacfa26e  (/usr/lib/libasan.so.8.0.0+0xa4f26e)
    #3 0x7b4fda422052 in SDL_DBus_Init_Spinlocked /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:153
    #4 0x7b4fda42212f in SDL_DBus_Init /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:175
    #5 0x7b4fda22825d in SDL_InitSubSystem_REAL /path/to/SDL-2.30.12/src/SDL.c:225
    #6 0x7b4fda2284a7 in SDL_Init_REAL /path/to/SDL-2.30.12/src/SDL.c:394
    #7 0x7b4fda244070 in SDL_Init_DEFAULT /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #8 0x7b4fda24d055 in SDL_Init /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #9 0x5fe9bf8a91b6 in main /path/to/SDL-bugtest/src/main.c:4
    #10 0x7b4fda035487  (/usr/lib/libc.so.6+0x27487) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #11 0x7b4fda03554b in __libc_start_main (/usr/lib/libc.so.6+0x2754b) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #12 0x5fe9bf8a90d4 in _start (/path/to/SDL-bugtest/build/SDL-bugtest+0x10d4) (BuildId: a68b569832c001aa6cc12658ee1341c78728de1f)

Indirect leak of 24 byte(s) in 1 object(s) allocated from:
    #0 0x7b4fda6fd721 in malloc /usr/src/debug/gcc/gcc/libsanitizer/asan/asan_malloc_linux.cpp:69
    #1 0x7b4fdad0d0c4  (<unknown module>)
    #2 0x7b4fda42201a in SDL_DBus_Init_Spinlocked /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:145
    #3 0x7b4fda42212f in SDL_DBus_Init /path/to/SDL-2.30.12/src/core/linux/SDL_dbus.c:175
    #4 0x7b4fda22825d in SDL_InitSubSystem_REAL /path/to/SDL-2.30.12/src/SDL.c:225
    #5 0x7b4fda2284a7 in SDL_Init_REAL /path/to/SDL-2.30.12/src/SDL.c:394
    #6 0x7b4fda244070 in SDL_Init_DEFAULT /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #7 0x7b4fda24d055 in SDL_Init /path/to/SDL-2.30.12/src/dynapi/SDL_dynapi_procs.h:88
    #8 0x5fe9bf8a91b6 in main /path/to/SDL-bugtest/src/main.c:4
    #9 0x7b4fda035487  (/usr/lib/libc.so.6+0x27487) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #10 0x7b4fda03554b in __libc_start_main (/usr/lib/libc.so.6+0x2754b) (BuildId: 695cfc6aac7d0f77bb7caba0ef01b2e868762b02)
    #11 0x5fe9bf8a90d4 in _start (/path/to/SDL-bugtest/build/SDL-bugtest+0x10d4) (BuildId: a68b569832c001aa6cc12658ee1341c78728de1f)

SUMMARY: AddressSanitizer: 2926 byte(s) leaked in 34 allocation(s).

```

</p>
</details> 

## Comment 2644354771

reporter (NONE) · ProgrammingRainbow · 2025-02-08T00:08:50Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2644354771

Does it need to be said that you should not be suppressing or hiding memory leaks at all. You should be shutting down correctly and cleaning up after yourself correctly. Reading the conversation above i wouldn't know these are C developers. There should be absolutely no reason that any memory is not freed correctly. I can't believe this needs to be stated. It is wild that people keep dancing around how to "fix" the problem by not fixing the problem. The problem is not false positives. The problem is failing to release your memory properly. Even the conversation about DBUS i felt like i was taking crazy pills. There was a conversation about NOT freeing the memory. Like it was suggested you shouldn't? This isn't javascript. You must clean up after yourself. that is what fsanatizer is telling you.

## Comment 2645750866

maintainer (COLLABORATOR) · icculus · 2025-02-08T14:49:12Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2645750866

You're not taking crazy pills, and you aren't wrong that memory _should_ be free'd.

But let's say we have a function in libSuperImportantFramework that we call:

```c
SuperImportantObject *CreateSuperImportantObject(void)
{
    char *temporary_work_space = malloc(100);
    SuperImportantObject *obj = malloc(sizeof (SuperImportantObject));  // we get this returned to us.
    // some other stuff happens here, they calculate something in temporary_work_space.
    return obj;   // ... but they didn't free temporary_work_space!
}

void FreeSuperImportantObject(SuperImportantObject *obj) { free(obj); }
```

Now, even though we _need_ the SuperImportantObject, and later on we correctly call FreeSuperImportantObject(), there's still a leak that is not our fault, and we _can't fix_ because the pointer is gone, and was never available to us.

Further imagine the maintainers of libSuperImportantFramework know about this and refuse to fix it. Maybe they say it's _intentional_, maybe they incorrectly think it's not a big deal, maybe they all died of old age and no one's maintaining the code anymore.

At this point, what are our options? We did our part right, and we can't change the SuperImportantFramework. All we can do is make it so your app doesn't have to see leaks that _also aren't your fault_.

(The other option is, of course, file a bug with libSuperImportantFramework and see if they'll change it, but as I'm sure you know, filing bugs isn't always a pleasant experience.)

I think it's possible that some of the OpenGL leaks might be legitimate bugs that the maintainers would fix. The leak in XrmIntialize has been there since _1988_. They aren't going to do anything about it.

## Comment 2645753497

maintainer (COLLABORATOR) · icculus · 2025-02-08T14:54:26Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2645753497

As for why this happens in sdl2-compat+SDL3 and not SDL2: SDL2 doesn't call XrmInitialize, because it was added in SDL3 to improve support for high-dpi displays.

And SDL2 (and at the moment, SDL3) doesn't use Wayland unless forced with the SDL_VIDEODRIVER=wayland environment variable, so even on a Wayland system, it'll default to using XWayland for various reasons...so the libdecor, etc, leaks wouldn't be visible before we told you to try forcing it. (This was my fault; I didn't know about those leaks when I suggested it.)

## Comment 2645969403

other (CONTRIBUTOR) · cgutman · 2025-02-08T22:39:15Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2645969403

> Even the conversation about DBUS i felt like i was taking crazy pills.

It is not intuitive at first glance to avoid cleaning up D-Bus, but there are very good reasons not to do so. As explicitly called out in the [D-Bus documentation](https://dbus.freedesktop.org/doc/api/html/group__DBusMemory.html):
> WARNING: dbus_shutdown() is NOT thread safe, it must be called while NO other threads are using D-Bus.

and:

> calling dbus_shutdown() from a library is almost certainly wrong, since you don't know what the rest of the app is up to.

The problem is that `dbus_shutdown()` immediately cleans up _all_ D-Bus state for the entire process, which could lead to a crash if the process is using D-Bus elsewhere. A library like SDL is a guest in the address space of a process and cannot be tearing down state that it cannot guarantee that it exclusively owns.

If `dbus_shutdown()` were to  synchronize with other D-Bus activity, then it _could_ be safe to cleanup in SDL. However, that's not the state of affairs now, and [upstream D-Bus developers recommend leaving it loaded to circumvent leak detection issues](https://gitlab.freedesktop.org/dbus/dbus/-/issues/495#note_2482723) (which SDL does in 3.2.4 now).

## Comment 2707309992

reporter (NONE) · ProgrammingRainbow · 2025-03-07T20:03:25Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2707309992

There still seems to be the same problem with SDL3 and SDL2-compat falsely hiding or misreporting memory leaks. I have written this small program to help people visualize it. It's interesting that memory safety is not being taken seriously, instead the answer seems to be lets just give false answers? I have stepped back waiting for the issue to fix itself because it was just absolutely too frustrating to try and communicate this, having had the Archlinux issue shutdown because Ryan kept miss representing what i was saying. And this thread here going no where. I hoped that internally it would be fix and or someone else who was better with communication could express the issue. But......

main.c
``` c
#include <SDL2/SDL.h>
#include <SDL2/SDL_image.h>
#include <SDL2/SDL_ttf.h>
#include <stdbool.h>
#include <stdio.h>

#define SDL_FLAGS SDL_INIT_EVERYTHING
#define IMG_FLAGS IMG_INIT_PNG
#define RENDERER_FLAGS SDL_RENDERER_ACCELERATED

#define WINDOW_TITLE "Memory Leak."
#define WINDOW_WIDTH 1280
#define WINDOW_HEIGHT 300

#define FONT_SIZE 300
#define FONT_COLOR {255, 255, 255, 255}

struct Game {
        SDL_Window *window;
        SDL_Renderer *renderer;
        SDL_Event event;
        bool is_running;
        TTF_Font *font;
        SDL_Surface *surface;
        SDL_Texture *image;
        SDL_Rect rect;
        unsigned int count;
};

bool game_new(struct Game **game);
void game_free(struct Game **game);
bool game_init_sdl(struct Game *g);
void game_events(struct Game *g);
bool game_update(struct Game *g);
void game_draw(const struct Game *g);
bool game_run(struct Game *g);

bool game_new(struct Game **game) {
    *game = calloc(1, sizeof(struct Game));
    if (*game == NULL) {
        fprintf(stderr, "Error in Calloc of New Game.\n");
        return false;
    }

    struct Game *g = *game;

    if (!game_init_sdl(g)) {
        return false;
    }

    g->font = TTF_OpenFont("fonts/freesansbold.ttf", FONT_SIZE);
    if (!g->font) {
        fprintf(stderr, "Error creating font: %s\n", TTF_GetError());
        return false;
    }

    g->is_running = true;
    g->count = 0;

    return true;
}

void game_free(struct Game **game) {
    if (*game) {
        struct Game *g = *game;

        // We don't ever need to free Textures or Surfaces!
        // if (g->image) {
        //     SDL_DestroyTexture(g->image);
        //     g->image = NULL;
        // }
        // if (g->surface) {
        //     SDL_FreeSurface(g->surface);
        //     g->surface = NULL;
        // }

        // I guess we need to free the font.
        if (g->font) {
            TTF_CloseFont(g->font);
            g->font = NULL;
        }

        // Why bother freeing renderer and window!
        // if (g->renderer) {
        //     SDL_DestroyRenderer(g->renderer);
        //     g->renderer = NULL;
        // }
        // if (g->window) {
        //     SDL_DestroyWindow(g->window);
        //     g->window = NULL;
        // }

        // Don't Quit Anything!
        // TTF_Quit();
        // IMG_Quit();
        // SDL_Quit();

        free(*game);
        *game = NULL;

        printf("all clean!\n");
    }
}

bool game_init_sdl(struct Game *g) {
    if (SDL_Init(SDL_FLAGS)) {
        fprintf(stderr, "Error initializing SDL2. %s\n", SDL_GetError());
        return false;
    }

    if ((IMG_Init(IMG_FLAGS) & IMG_FLAGS) != IMG_FLAGS) {
        fprintf(stderr, "Error initializing SDL_image. %s\n", IMG_GetError());
        return false;
    }

    if (TTF_Init()) {
        fprintf(stderr, "Error initializing SDL_ttf: %s\n", TTF_GetError());
        return false;
    }

    g->window = SDL_CreateWindow(WINDOW_TITLE, SDL_WINDOWPOS_CENTERED,
                                 SDL_WINDOWPOS_CENTERED, WINDOW_WIDTH,
                                 WINDOW_HEIGHT, 0);
    if (!g->window) {
        fprintf(stderr, "Error creating SDL_Window. %s\n", SDL_GetError());
        return false;
    }

    g->renderer = SDL_CreateRenderer(g->window, -1, RENDERER_FLAGS);
    if (!g->renderer) {
        fprintf(stderr, "Error creating SDL_Renderer. %s\n", SDL_GetError());
        return false;
    }

    return true;
}

void game_events(struct Game *g) {
    while (SDL_PollEvent(&g->event)) {
        switch (g->event.type) {
        case SDL_QUIT:
            g->is_running = false;
            break;
        case SDL_KEYDOWN:
            switch (g->event.key.keysym.scancode) {
            case SDL_SCANCODE_ESCAPE:
                g->is_running = false;
                break;
            default:
                break;
            }
            break;
        default:
            break;
        }
    }
}

bool game_update(struct Game *g) {
    // We don't ever need to free Textures or Surfaces!
    // if (g->image) {
    //     SDL_DestroyTexture(g->image);
    //     g->image = NULL;
    // }
    // if (g->surface) {
    //     SDL_FreeSurface(g->surface);
    //     g->surface = NULL;
    // }

    int str_length = snprintf(NULL, 0, "%d", g->count) + 1;
    char str_array[str_length];
    snprintf(str_array, (size_t)str_length, "%d", g->count);

    g->surface =
        TTF_RenderText_Blended(g->font, str_array, (SDL_Color)FONT_COLOR);
    if (!g->surface) {
        fprintf(stderr, "Error creating a surface: %s\n", TTF_GetError());
        return false;
    }

    g->image = SDL_CreateTextureFromSurface(g->renderer, g->surface);
    if (!g->image) {
        fprintf(stderr, "Error creating a texture: %s\n", SDL_GetError());
        return false;
    }

    if (SDL_QueryTexture(g->image, NULL, NULL, &g->rect.w, &g->rect.h)) {
        fprintf(stderr, "Error while querying texture: %s\n", SDL_GetError());
        return false;
    }

    g->count++;

    return true;
}

void game_draw(const struct Game *g) {
    SDL_RenderClear(g->renderer);

    SDL_RenderCopy(g->renderer, g->image, NULL, &g->rect);

    SDL_RenderPresent(g->renderer);
}

bool game_run(struct Game *g) {
    while (g->is_running) {
        game_events(g);

        if (!game_update(g)) {
            return false;
        }

        game_draw(g);

        SDL_Delay(16);
    }

    return true;
}

int main(void) {
    bool exit_status = EXIT_FAILURE;

    struct Game *game = NULL;

    if (game_new(&game)) {
        if (game_run(game)) {
            exit_status = EXIT_SUCCESS;
        }
    }

    game_free(&game);

    return exit_status;
}
```
``` shell
gcc -g3 -fsanitize=address -fsanitize-address-use-after-scope -lSDL2 -lSDL2_image -lSDL2_ttf main.
c -o memory_leaks && ./memory_leaks
```
Notice how i am not shutting anything down or cleaning anything up except for TTF_CloseFont. I am also creating a new surface and texture every frame but not freeing the memory already allocated. This causes the ram usage to grow until eventually linux sees Alacritty is doing something it shouldn't and just shuts it down. But fsanitize says there is no issue? Now if i don't free the font fsanitizer does care. And if i don't free game then it does. But almost all the SDL2 stuff is falsely reporting no issue. This is not the first time i have said this. I feel like I'm shouting at clouds.

Versions: sdl2-compat-2.32.52 sdl2_image-2.8.8 sdl2_ttf-2.24.0

## Comment 2707387719

maintainer (COLLABORATOR) · slouken · 2025-03-07T20:31:30Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2707387719

Do you have the same problem if you use SDL3 directly?

## Comment 2707450505

reporter (NONE) · ProgrammingRainbow · 2025-03-07T21:01:50Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2707450505

It looks like I need to free surfaces. But the rest is the same. This is archlinux so SDL3_image and SDL3_ttf are from aur. I hope this is all correct SDL3 i just grabbed some code snippets i had from my test SDL3.

sdl3_main.c
``` c
#include <SDL3/SDL.h>
#include <SDL3_image/SDL_image.h>
#include <SDL3_ttf/SDL_ttf.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define SDL_FLAGS SDL_INIT_VIDEO
#define IMG_FLAGS IMG_INIT_PNG

#define WINDOW_TITLE "Memory Leak."
#define WINDOW_WIDTH 1280
#define WINDOW_HEIGHT 300

#define FONT_SIZE 300
#define FONT_COLOR {255, 255, 255, 255}

struct Game {
        SDL_Window *window;
        SDL_Renderer *renderer;
        SDL_Event event;
        bool is_running;
        TTF_Font *font;
        SDL_Surface *surface;
        SDL_Texture *image;
        SDL_FRect rect;
        unsigned int count;
};

bool game_new(struct Game **game);
void game_free(struct Game **game);
bool game_init_sdl(struct Game *g);
void game_events(struct Game *g);
bool game_update(struct Game *g);
void game_draw(const struct Game *g);
bool game_run(struct Game *g);

bool game_new(struct Game **game) {
    *game = calloc(1, sizeof(struct Game));
    if (*game == NULL) {
        fprintf(stderr, "Error in Calloc of New Game.\n");
        return false;
    }

    struct Game *g = *game;

    if (!game_init_sdl(g)) {
        return false;
    }

    g->font = TTF_OpenFont("fonts/freesansbold.ttf", FONT_SIZE);
    if (!g->font) {
        fprintf(stderr, "Error creating font: %s\n", SDL_GetError());
        return false;
    }

    g->is_running = true;
    g->count = 0;

    return true;
}

void game_free(struct Game **game) {
    if (*game) {
        struct Game *g = *game;

        // We don't ever need to free Textures!
        // if (g->image) {
        //     SDL_DestroyTexture(g->image);
        //     g->image = NULL;
        // }
        if (g->surface) {
            SDL_DestroySurface(g->surface);
            g->surface = NULL;
        }

        // I guess we need to free the font.
        if (g->font) {
            TTF_CloseFont(g->font);
            g->font = NULL;
        }

        // Why bother freeing renderer and window!
        // if (g->renderer) {
        //     SDL_DestroyRenderer(g->renderer);
        //     g->renderer = NULL;
        // }
        // if (g->window) {
        //     SDL_DestroyWindow(g->window);
        //     g->window = NULL;
        // }

        // Don't Quit Anything!
        // TTF_Quit();
        // SDL_Quit();

        free(*game);
        *game = NULL;

        printf("all clean!\n");
    }
}

bool game_init_sdl(struct Game *g) {
    if (!SDL_Init(SDL_FLAGS)) {
        fprintf(stderr, "Error initializing SDL3. %s\n", SDL_GetError());
        return false;
    }

    if (!TTF_Init()) {
        fprintf(stderr, "Error initializing SDL_ttf: %s\n", SDL_GetError());
        return false;
    }

    g->window = SDL_CreateWindow(WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, 0);
    if (!g->window) {
        fprintf(stderr, "Error creating window: %s\n", SDL_GetError());
        return false;
    }

    g->renderer = SDL_CreateRenderer(g->window, NULL);
    if (!g->renderer) {
        fprintf(stderr, "Error creating renderer: %s\n", SDL_GetError());
        return false;
    }

    return true;
}

void game_events(struct Game *g) {
    while (SDL_PollEvent(&g->event)) {
        switch (g->event.type) {
        case SDL_EVENT_QUIT:
            g->is_running = false;
            break;
        case SDL_EVENT_KEY_DOWN:
            switch (g->event.key.scancode) {
            case SDL_SCANCODE_ESCAPE:
                g->is_running = false;
                break;
            default:
                break;
            }
            break;
        default:
            break;
        }
    }
}

bool game_update(struct Game *g) {
    // We don't ever need to free Textures!
    // if (g->image) {
    //     SDL_DestroyTexture(g->image);
    //     g->image = NULL;
    // }
    if (g->surface) {
        SDL_DestroySurface(g->surface);
        g->surface = NULL;
    }

    int str_length = snprintf(NULL, 0, "%d", g->count) + 1;
    char str_array[str_length];
    snprintf(str_array, (size_t)str_length, "%d", g->count);

    g->surface =
        TTF_RenderText_Blended(g->font, str_array, 0, (SDL_Color)FONT_COLOR);
    if (!g->surface) {
        fprintf(stderr, "Error creating Surface: %s\n", SDL_GetError());
        return false;
    }

    g->image = SDL_CreateTextureFromSurface(g->renderer, g->surface);
    if (!g->image) {
        fprintf(stderr, "Error creating a texture: %s\n", SDL_GetError());
        return false;
    }

    if (!SDL_GetTextureSize(g->image, &g->rect.w, &g->rect.h)) {
        fprintf(stderr, "Error getting texture size: %s\n", SDL_GetError());
        return false;
    }

    g->count++;

    return true;
}

void game_draw(const struct Game *g) {
    SDL_RenderClear(g->renderer);

    SDL_RenderTexture(g->renderer, g->image, NULL, &g->rect);

    SDL_RenderPresent(g->renderer);
}

bool game_run(struct Game *g) {
    while (g->is_running) {
        game_events(g);

        if (!game_update(g)) {
            return false;
        }

        game_draw(g);

        SDL_Delay(16);
    }

    return true;
}

int main(void) {
    bool exit_status = EXIT_FAILURE;

    struct Game *game = NULL;

    if (game_new(&game)) {
        if (game_run(game)) {
            exit_status = EXIT_SUCCESS;
        }
    }

    game_free(&game);

    return exit_status;
}
```
``` shell
gcc -g3 -fsanitize=address -fsanitize-address-use-after-scope -lSDL3 -lSDL3_image -lSDL3_ttf sdl3_main.c -o memory_leaks && ./memory_leaks
```

## Comment 2707526713

maintainer (COLLABORATOR) · icculus · 2025-03-07T21:50:54Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2707526713

> It looks like I need to free surfaces

Do we have a list somewhere of "things we should automatically destroy on SDL_Quit but currently don't"? I don't know if this ever made it into the bug tracker.

## Comment 2707528769

maintainer (COLLABORATOR) · slouken · 2025-03-07T21:52:22Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2707528769

I don't think we ever made a list, but windows, renderers, and textures are all automatically freed. Surfaces are not, so the results for the SDL3 program are what I'd expect if SDL_Quit() were being called, but it isn't in this case.

## Comment 2707563888

reporter (NONE) · ProgrammingRainbow · 2025-03-07T22:05:14Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2707563888

If there is some internal SDL garbage collector that is going and freeing all the textures that are no longer reachable should that be explained somewhere in the documentation? I'm also just curious how it's determined that a texture is no longer reachable. Just curious.

## Comment 2707679725

maintainer (COLLABORATOR) · icculus · 2025-03-07T23:08:46Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2707679725

No garbage collector checking reachability, but it does keep a list of textures that haven't been destroyed yet, and destroys them during SDL_Quit.

## Comment 2708405100

maintainer (COLLABORATOR) · slouken · 2025-03-08T17:24:28Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2708405100

I don't know why address sanitizer doesn't find the leaks, but if you use SDL's test memory tracking you see all the leaks you would expect:
```c++
#include <SDL3/SDL.h>
#include <SDL3/SDL_test.h>
#include <SDL3_image/SDL_image.h>
#include <SDL3_ttf/SDL_ttf.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#define SDL_FLAGS SDL_INIT_VIDEO
#define IMG_FLAGS IMG_INIT_PNG

#define WINDOW_TITLE "Memory Leak."
#define WINDOW_WIDTH 1280
#define WINDOW_HEIGHT 300

#define FONT_SIZE 300
#define FONT_COLOR {255, 255, 255, 255}

struct Game {
        SDL_Window *window;
        SDL_Renderer *renderer;
        SDL_Event event;
        bool is_running;
        TTF_Font *font;
        SDL_Surface *surface;
        SDL_Texture *image;
        SDL_FRect rect;
        unsigned int count;
};

bool game_new(struct Game **game);
void game_free(struct Game **game);
bool game_init_sdl(struct Game *g);
void game_events(struct Game *g);
bool game_update(struct Game *g);
void game_draw(const struct Game *g);
bool game_run(struct Game *g);

bool game_new(struct Game **game) {
    *game = calloc(1, sizeof(struct Game));
    if (*game == NULL) {
        fprintf(stderr, "Error in Calloc of New Game.\n");
        return false;
    }

    struct Game *g = *game;

    if (!game_init_sdl(g)) {
        return false;
    }

    g->font = TTF_OpenFont("fonts/freesansbold.ttf", FONT_SIZE);
    if (!g->font) {
        fprintf(stderr, "Error creating font: %s\n", SDL_GetError());
        return false;
    }

    g->is_running = true;
    g->count = 0;

    return true;
}

void game_free(struct Game **game) {
    if (*game) {
        struct Game *g = *game;

        // We don't ever need to free Textures!
        // if (g->image) {
        //     SDL_DestroyTexture(g->image);
        //     g->image = NULL;
        // }
        if (g->surface) {
            SDL_DestroySurface(g->surface);
            g->surface = NULL;
        }

        // I guess we need to free the font.
        if (g->font) {
            TTF_CloseFont(g->font);
            g->font = NULL;
        }

        // Why bother freeing renderer and window!
        // if (g->renderer) {
        //     SDL_DestroyRenderer(g->renderer);
        //     g->renderer = NULL;
        // }
        // if (g->window) {
        //     SDL_DestroyWindow(g->window);
        //     g->window = NULL;
        // }

        // Don't Quit Anything!
        // TTF_Quit();
        // SDL_Quit();

        free(*game);
        *game = NULL;

        printf("all clean!\n");
    }
}

bool game_init_sdl(struct Game *g) {
    if (!SDL_Init(SDL_FLAGS)) {
        fprintf(stderr, "Error initializing SDL3. %s\n", SDL_GetError());
        return false;
    }

    if (!TTF_Init()) {
        fprintf(stderr, "Error initializing SDL_ttf: %s\n", SDL_GetError());
        return false;
    }

    g->window = SDL_CreateWindow(WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, 0);
    if (!g->window) {
        fprintf(stderr, "Error creating window: %s\n", SDL_GetError());
        return false;
    }

    g->renderer = SDL_CreateRenderer(g->window, NULL);
    if (!g->renderer) {
        fprintf(stderr, "Error creating renderer: %s\n", SDL_GetError());
        return false;
    }

    return true;
}

void game_events(struct Game *g) {
    while (SDL_PollEvent(&g->event)) {
        switch (g->event.type) {
        case SDL_EVENT_QUIT:
            g->is_running = false;
            break;
        case SDL_EVENT_KEY_DOWN:
            switch (g->event.key.scancode) {
            case SDL_SCANCODE_ESCAPE:
                g->is_running = false;
                break;
            default:
                break;
            }
            break;
        default:
            break;
        }
    }
}

bool game_update(struct Game *g) {
    // We don't ever need to free Textures!
    // if (g->image) {
    //     SDL_DestroyTexture(g->image);
    //     g->image = NULL;
    // }
    if (g->surface) {
        SDL_DestroySurface(g->surface);
        g->surface = NULL;
    }

    int str_length = snprintf(NULL, 0, "%d", g->count) + 1;
    char str_array[str_length];
    snprintf(str_array, (size_t)str_length, "%d", g->count);

    g->surface =
        TTF_RenderText_Blended(g->font, str_array, 0, (SDL_Color)FONT_COLOR);
    if (!g->surface) {
        fprintf(stderr, "Error creating Surface: %s\n", SDL_GetError());
        return false;
    }

    g->image = SDL_CreateTextureFromSurface(g->renderer, g->surface);
    if (!g->image) {
        fprintf(stderr, "Error creating a texture: %s\n", SDL_GetError());
        return false;
    }

    if (!SDL_GetTextureSize(g->image, &g->rect.w, &g->rect.h)) {
        fprintf(stderr, "Error getting texture size: %s\n", SDL_GetError());
        return false;
    }

    g->count++;

    return true;
}

void game_draw(const struct Game *g) {
    SDL_RenderClear(g->renderer);

    SDL_RenderTexture(g->renderer, g->image, NULL, &g->rect);

    SDL_RenderPresent(g->renderer);
}

bool game_run(struct Game *g) {
    while (g->is_running) {
        game_events(g);

        if (!game_update(g)) {
            return false;
        }

        game_draw(g);

        SDL_Delay(16);
    }

    return true;
}

int main(void) {
    bool exit_status = EXIT_FAILURE;

    struct Game *game = NULL;

    SDLTest_TrackAllocations();

    if (game_new(&game)) {
        if (game_run(game)) {
            exit_status = EXIT_SUCCESS;
        }
    }

    game_free(&game);

    SDLTest_LogAllocations();

    return exit_status;
}
```
```sh
gcc -g3 -fsanitize=undefined -fsanitize=leak -fsanitize=address -fsanitize-address-use-after-scope sdl3_main.c -lSDL3 -lSDL3_test -lSDL3_image -lSDL3_ttf -lunwind -o memory_leaks && ./memory_leaks
```

## Comment 2708405854

maintainer (COLLABORATOR) · slouken · 2025-03-08T17:26:35Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2708405854

If you uncomment TTF_Quit() and SDL_Quit(), this checks out clean, since as we noted SDL automatically cleans up windows, renderers, and textures in SDL_Quit().

## Comment 2708411026

maintainer (COLLABORATOR) · slouken · 2025-03-08T17:38:46Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2708411026

At this point, I would suggest reporting this upstream on the address sanitizer bug tracker.

## Comment 2717788415

other (NONE) · jengelh · 2025-03-12T12:51:57Z · https://github.com/libsdl-org/sdl2-compat/issues/255#issuecomment-2717788415

Sounds like we should demand from e.g. x11/dbus that init/shutdown gets reference counted at the very least.
