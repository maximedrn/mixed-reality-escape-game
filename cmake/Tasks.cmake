cmake_minimum_required(VERSION 3.20)

get_filename_component(ROOT "${CMAKE_CURRENT_LIST_DIR}/.." ABSOLUTE)
set(UNITY_DIR "${ROOT}/Unity")
set(SRC "${UNITY_DIR}/Assets/_Game")

if(NOT DEFINED TASK)
    set(TASK "check")
endif()

function(run_dotnet)
    find_program(DOTNET NAMES dotnet REQUIRED)
    execute_process(
        COMMAND "${DOTNET}" ${ARGN}
        WORKING_DIRECTORY "${ROOT}"
        RESULT_VARIABLE STATUS
        COMMAND_ECHO STDOUT
        COMMAND_ERROR_IS_FATAL ANY
    )

    if(NOT STATUS EQUAL 0)
        message(FATAL_ERROR "dotnet command failed: ${STATUS}")
    endif()
endfunction()

function(find_unity_solution OUTPUT)
    file(GLOB SOLUTIONS "${UNITY_DIR}/*.slnx")

    if(NOT SOLUTIONS)
        file(GLOB SOLUTIONS "${UNITY_DIR}/*.sln")
    endif()

    if(NOT SOLUTIONS)
        message(FATAL_ERROR
            "Unity solution not found. Regenerate project files in Unity."
        )
    endif()

    list(GET SOLUTIONS 0 SOLUTION)
    set(${OUTPUT} "${SOLUTION}" PARENT_SCOPE)
endfunction()

function(setup)
    run_dotnet(tool restore)
endfunction()

function(format_code)
    run_dotnet(csharpier format "${SRC}")
endfunction()

function(check_format)
    run_dotnet(csharpier check "${SRC}")
endfunction()

function(lint)
    find_unity_solution(SOLUTION)

    set(OPTIONS
        --include "${SRC}"
        --verify-no-changes
        --severity warn
    )

    if(VERBOSE)
        list(APPEND OPTIONS --verbosity diagnostic)
    endif()

    run_dotnet(
        format style "${SOLUTION}"
        ${OPTIONS}
    )

    run_dotnet(
        format analyzers "${SOLUTION}"
        ${OPTIONS}
    )
endfunction()

function(motion_setup)
    find_program(UV NAMES uv REQUIRED)

    execute_process(
        COMMAND "${UV}" sync --locked
            --project "${ROOT}/tools/motion"
        WORKING_DIRECTORY "${ROOT}"
        COMMAND_ERROR_IS_FATAL ANY
    )
endfunction()

function(motion_check)
    find_program(UV NAMES uv REQUIRED)

    execute_process(
        COMMAND "${UV}" run
            --locked
            --project "${ROOT}/tools/motion"
            poe -C "${ROOT}/tools/motion" check
        WORKING_DIRECTORY "${ROOT}"
        COMMAND_ERROR_IS_FATAL ANY
    )
endfunction()

function(python_lint)
    find_program(UV NAMES uv REQUIRED)

    execute_process(
        COMMAND "${UV}" run --locked --project "${ROOT}/tools/lint"
            poe -C "${ROOT}/tools/lint" check
        WORKING_DIRECTORY "${ROOT}"
        COMMAND_ERROR_IS_FATAL ANY
    )
endfunction()

if(TASK STREQUAL "setup")
    setup()

elseif(TASK STREQUAL "format")
    format_code()

elseif(TASK STREQUAL "check-format")
    check_format()

elseif(TASK STREQUAL "lint")
    lint()

elseif(TASK STREQUAL "check")
    check_format()
    lint()

elseif(TASK STREQUAL "motion-setup")
    motion_setup()

elseif(TASK STREQUAL "motion-check")
    motion_check()

elseif(TASK STREQUAL "python-lint")
    python_lint()

else()
    message(FATAL_ERROR "Unknown task: ${TASK}")
endif()
