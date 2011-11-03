/* GemRB - Infinity Engine Emulator
 * Copyright (C) 2003-2011 The GemRB Project
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * as published by the Free Software Foundation; either version 2
 * of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 *
 *
 */
#import <SDL.h>
#import "CocoaWrapper.h"

// SDL 1.3 has its own App Delegate, but curently all it does is what this delegate category is doing
// SDL is nice enough to check if a delegate exists prior to assigning its own.

#if TARGET_OS_IPHONE > 0
#import <UIKit/UIKit.h>
#import <QuartzCore/QuartzCore.h>

@interface SDL_UIKit_ModifierKeyButton : UIButton {
@private
    SDLMod _modifierKey;
}
@property(nonatomic, assign, getter = modifierKey, setter = setModifierKey:) SDLMod _modifierKey;

- (void)toggleModifier;
@end

@implementation SDL_UIKit_ModifierKeyButton
@synthesize _modifierKey;
#pragma mark Parent Method Overrides

- (id)initWithFrame:(CGRect)frame
{
	self = [super initWithFrame:frame];
	if (self) {
		_modifierKey = KMOD_NONE;

		//custom drawing
		self.backgroundColor = [UIColor colorWithRed:0.196 green:0.3098 blue:0.52 alpha:1.0];
		self.titleLabel.textColor = [UIColor grayColor];
		self.titleLabel.font = [UIFont systemFontOfSize:24];
		self.layer.cornerRadius = 10;
		self.layer.borderWidth = 2;
		self.layer.borderColor = [UIColor grayColor].CGColor;
		self.clipsToBounds = YES;

		[self addTarget:self action:@selector(toggleModifier) forControlEvents:UIControlEventTouchDown];
	}
	return self;
}

- (BOOL)selected
{
	return (BOOL)(SDL_GetModState() & _modifierKey);
}

- (void)setSelected:(BOOL)selected
{
	if (selected) SDL_SetModState(SDL_GetModState() | _modifierKey);
	else SDL_SetModState(SDL_GetModState() & ~_modifierKey);
}

- (void)toggleModifier
{
	[self setSelected:!self.selected];
}

@end

// need a custom accessory view for the keybaord (for ctrl key modifier)
@interface UITextField (KeyboardAccesory)
-(UIView *)inputAccessoryView;// override UIKit and force our own
@end

@implementation UITextField (KeyboardAccesory)
- (UIView *)inputAccessoryView
{
	static UIView* accessoryView = nil;
	if (!accessoryView){
		CGRect accessFrame = CGRectMake(0.0, 0.0, [UIScreen mainScreen].bounds.size.width, 77.0);
        accessoryView = [[UIView alloc] initWithFrame:accessFrame];
        accessoryView.backgroundColor = [UIColor colorWithRed:0.5 green:0.5 blue:0.5 alpha:0.5];
		CGFloat xSpacing = 20.0;
		CGFloat xPos = xSpacing;
		//ctrl key
        SDL_UIKit_ModifierKeyButton *ctrlButton = [[SDL_UIKit_ModifierKeyButton alloc] initWithFrame:CGRectMake(xPos, 20.0, 120.0, 40.0)];
		ctrlButton.modifierKey = KMOD_LCTRL;
        [ctrlButton setTitle: @"Ctrl" forState:UIControlStateNormal];
        [accessoryView addSubview:ctrlButton];
		[ctrlButton release];
		//alt key
		xPos += xSpacing;
		SDL_UIKit_ModifierKeyButton *altButton = [[SDL_UIKit_ModifierKeyButton alloc] initWithFrame:CGRectMake(xPos, 20.0, 120.0, 40.0)];
		altButton.modifierKey = KMOD_LALT;
        [altButton setTitle: @"Alt" forState:UIControlStateNormal];
        [accessoryView addSubview:altButton];
		[altButton release];
	}
    return accessoryView;
}
@end
/*
Mac OS X wrapper
*/
#elif TARGET_OS_MAC
@interface CocoaWrapper (SDLTerminate)
- (NSApplicationTerminateReply)applicationShouldTerminate:(NSApplication *)sender;
@end

@implementation CocoaWrapper (SDLTerminate)
- (NSApplicationTerminateReply)applicationShouldTerminate:(NSApplication *) __unused sender
{
    NSLog(@"Received terminate request. Dispatching SDL_QUIT event...");
    SDL_Event event;
    event.type = SDL_QUIT;
    SDL_PushEvent(&event);
    // we deny the application request to terminate.
    // this way we can let GemRB handle quit event so we can save before exit etc.
    return NSTerminateCancel;
}
@end
#endif
