# Research only proof of concept

This repository contains a research only proof of concept demonstrating design weaknesses in Microsoft Windows UI trust and recovery behavior

You may download run and inspect this project only in its original unmodified form  
Modification derivative works or redistribution of modified versions are prohibited

All use is governed by the Custom Research & Demonstration License in the LICENSE file  
Any use outside those terms is unauthorized and the sole responsibility of the user

This project exists to raise awareness of architectural issues not for deployment persistence or real world exploitation

If you are looking to extend weaponize or repurpose this code you are not permitted to do so

## Overview

Proof of concept highlighting critical weaknesses in Windows UI trust and recovery design

This project demonstrates that a standard user mode process without admin rights drivers or kernel exploits can convincingly lock a Windows session It does so by switching the user to a separate desktop presenting a full screen system impersonating crash screen and suppressing Task Manager to block the primary recovery path users rely on

While this PoC allows recovery via sign out or power off the underlying design flaws it exposes are far more serious The same mechanisms shown here can be combined with persistence session re entry or startup execution to create situations where recovery becomes extremely difficult for non technical users

Nothing here relies on undefined behavior or exploits only documented APIs and expected OS behavior  
That is the problem

This repository exists to raise awareness that Windows currently allows user space applications to

Impersonate critical system failure states  
Obstruct built in recovery tools  
Abuse desktop isolation in ways users cannot easily distinguish from real system failure  

These are architectural issues not edge cases
