/*
This file is part of Telegram Desktop,
the official desktop application for the Telegram messaging service.

For license and copyright information please follow this link:
https://github.com/telegramdesktop/tdesktop/blob/master/LEGAL
*/
#pragma once

namespace TouchBar {

enum class Option {
	PinnedChats,
	EmojiButton,
	RecentEmoji,
	CustomEmoji,
	CustomEmojiFirst,
	FormatButton,
};

[[nodiscard]] bool OptionEnabled(Option option);
void SetOptionEnabled(Option option, bool enabled);
[[nodiscard]] rpl::producer<> OptionsChanges();

} // namespace TouchBar
