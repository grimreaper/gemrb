class GameControl;

#ifndef GAMECONTROL_H
#define GAMECONTROL_H

#include "Control.h"
#include "Interface.h"
#include "PathFinder.h"
#include "Dialog.h"

#ifdef WIN32

#ifdef GEM_BUILD_DLL
#define GEM_EXPORT __declspec(dllexport)
#else
#define GEM_EXPORT __declspec(dllimport)
#endif

#else
#define GEM_EXPORT
#endif

#ifndef _DEBUG
#define _DEBUG
#endif

class GEM_EXPORT GameControl : public Control {
public:
	GameControl(void);
	~GameControl(void);
public:
	/** Draws the Control on the Output Display */
	void Draw(unsigned short x, unsigned short y);
	/** Sets the Text of the current control */
	int SetText(const char* string, int pos = 0);
	/** Sets the current area to Display */
	Map *SetCurrentArea(int Index);
	/** Sets the InfoTextColor, used in PST
	*/
	void SetInfoTextColor(Color color);
private:
	int MapIndex;
	Actor* lastActor;
	std::vector< Actor*> selected;
	std::vector< Actor*> highlighted;
	std::vector< Scriptable*> infoTexts;
	Color* InfoTextPalette;
	bool DrawSelectionRect;
	bool MouseIsDown;
	Region SelectionRect;
	short StartX, StartY;
public:
	Door* overDoor;
	Container* overContainer;
	InfoPoint* overInfoPoint;
private:
	unsigned char lastCursor;
	short moveX, moveY;
	unsigned short lastMouseX, lastMouseY;
	int DebugFlags;
	short pfsX, pfsY;
	PathNode* drawPath;
	unsigned long AIUpdateCounter;
	bool DisableMouse;
	bool GUIEnabled;
public: //Events
	/** Key Press Event */
	void OnKeyPress(unsigned char Key, unsigned short Mod);
	/** Key Release Event */
	void OnKeyRelease(unsigned char Key, unsigned short Mod);
	/** Mouse Over Event */
	void OnMouseOver(unsigned short x, unsigned short y);
	/** Mouse Button Down */
	void OnMouseDown(unsigned short x, unsigned short y, unsigned char Button,
		unsigned short Mod);
	/** Mouse Button Up */
	void OnMouseUp(unsigned short x, unsigned short y, unsigned char Button,
		unsigned short Mod);
	/** Special Key Press */
	void OnSpecialKeyPress(unsigned char Key);
private:
	void CalculateSelection(unsigned short x, unsigned short y);
	void ResizeDel(Window* win, unsigned char type);
	void ResizeAdd(Window* win, unsigned char type);
	unsigned char LeftCount, BottomCount, RightCount, TopCount;
	DialogState* ds;
	Dialog* dlg;
	bool ChangeArea;
public:
	Actor* speaker, * target;
	char Destination[33], EntranceName[33];
	bool Dialogue;
public:
	/* Selects one or all PC */
	void SelectActor(int whom);
	void SetCutSceneMode(bool active);
	void HideGUI();
	void UnhideGUI();
	void TryToTalk(Actor *source, Actor *target);
	void InitDialog(Actor* speaker, Actor* target, const char* dlgref);
	void EndDialog();
	void DialogChoose(int choose);
	/** finds the first true condition in a dialog */
	int FindFirstState(Scriptable* target, Dialog* dlg);
	void DisplayString(Scriptable* target);
	/* Displays a string in the textarea */
	void DisplayString(char* Text);
	Actor *GetLastActor() { return lastActor; }
private:
	void ChangeMap();
	/* evaluates a dialog trigger block */
	bool EvaluateDialogTrigger(Scriptable* target, DialogString* trigger);
};

#endif
