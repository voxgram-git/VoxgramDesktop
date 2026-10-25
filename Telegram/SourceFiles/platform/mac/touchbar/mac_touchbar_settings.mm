/*
This file is part of Telegram Desktop,
the official desktop application for the Telegram messaging service.

For license and copyright information please follow this link:
https://github.com/telegramdesktop/tdesktop/blob/master/LEGAL
*/
#include "platform/mac/touchbar/mac_touchbar_settings.h"

#include "core/application.h"
#include "core/core_settings.h"

namespace TouchBar {
namespace {

[[nodiscard]] std::string_view OptionKey(Option option) {
	switch (option) {
	case Option::PinnedChats: return "touchbar-pinned-chats";
	case Option::EmojiButton: return "touchbar-emoji-button";
	case Option::RecentEmoji: return "touchbar-recent-emoji";
	case Option::CustomEmoji: return "touchbar-custom-emoji";
	case Option::CustomEmojiFirst: return "touchbar-custom-emoji-first";
	case Option::FormatButton: return "touchbar-format-button";
	}
	Unexpected("Option in TouchBar::OptionKey.");
}

[[nodiscard]] rpl::event_stream<> &OptionsChangesStream() {
	static auto result = rpl::event_stream<>();
	return result;
}

} // namespace

bool OptionEnabled(Option option) {
	return Core::App().settings().readPref<bool>(OptionKey(option), true);
}

void SetOptionEnabled(Option option, bool enabled) {
	if (OptionEnabled(option) == enabled) {
		return;
	}
	Core::App().settings().writePref<bool>(OptionKey(option), enabled);
	Core::App().saveSettingsDelayed();
	OptionsChangesStream().fire({});
}

rpl::producer<> OptionsChanges() {
	return OptionsChangesStream().events();
}

} // namespace TouchBar
